# -*- coding:utf8 -*-
import logging
import os
import pickle
from tempfile import NamedTemporaryFile

import numpy as np

import tensorflow as tf
from tensorflow.core.framework.graph_pb2 import GraphDef
from tensorflow.tools.graph_transforms import TransformGraph
from utensor_cgen.frontend import FrontendSelector
from utensor_cgen.ir import uTensorGraph
from utensor_cgen.transformer.optimizer import RefCntOptimizer
from utensor_cgen.transformer.pipeline import TransformerPipeline
from utensor_cgen.utils import NamescopedKWArgsParser

from .operators import OperatorFactory
from .snippets import (CommentSnippet, ContextGlobalArrayContainer,
                       ContextHeaderSnippet, ContextSnippetsContainer,
                       CreateTensorBinarySnippet, CreateTensorIdxSnippet)
from .snippets.composer import Composer

__all__ = ["CodeGenerator"]
_logger = logging.getLogger('utensor-cli')

class CodeGenerator(object):
  def __init__(self, model_file,
               idx_dir,
               embed_data_dir,
               trans_methods, # [(trans_name, kwargs),...]
               output_nodes,
               save_graph=False,
               debug_cmt=False):
    self.model_file = model_file
    if not os.path.exists(idx_dir):
      os.makedirs(idx_dir)
    self.idx_dir = idx_dir
    self.embed_data_dir = embed_data_dir.rstrip("/")
    self.trans_methods = trans_methods
    self.output_nodes = output_nodes
    self.save_graph = save_graph
    self.debug_cmt = debug_cmt

  def generate(self, src_fname):
    _, ext = os.path.splitext(self.model_file)
    parser_cls = FrontendSelector.select_parser(ext)
    ugraph = parser_cls.parse(self.model_file, self.output_nodes)
    self._generate(src_fname, ugraph)

  def _generate(self, src_fname, ugraph):
    """Generate source and header files
    """
    fname, _ = os.path.splitext(src_fname)
    graph_name, _ = os.path.splitext(os.path.basename(self.model_file))
    guard_name = fname.replace('/', '_')
    weightheader_fname = '{}_weight.hpp'.format(fname)
    header_snippet = ContextHeaderSnippet(guard_name, graph_name)
    weight_container = ContextGlobalArrayContainer()
    composer = Composer()
    header_fname = '{}.hpp'.format(fname)
    header_name = os.path.basename(header_fname)
    weightheader_name = os.path.basename(weightheader_fname)
    container = ContextSnippetsContainer(graph_name, header_name, weightheader_name)

    opFactory = OperatorFactory()

    self._check_non_quantized(ugraph)
    _logger.info("Transforming graph: %s", self.model_file)
    def formatter(name, kwargs):
      if kwargs:
        return '{}({})'.format(
          name,
          ', '.join(['{}={!r}'.format(k, v) for k, v in kwargs.items()])
        )
      else:
        return name
    _logger.info("Transform pipeline: %s", ' -> '.join([
      formatter(name, kwargs) for name, kwargs in self.trans_methods
      ])
    )
    quant_ugraph = self._transform_graph(ugraph,
                                         self.trans_methods)
    _logger.info('Graph transormation done')

    if self.save_graph:
      _logger.info('Saving transformed graph')
      pkl_fname = "quant_{}.pkl".format(graph_name)
      with open(pkl_fname, 'wb') as fid:
        pickle.dump(quant_ugraph, fid)
      _logger.info('{} saved'.format(pkl_fname))

    for op_id, op_name in enumerate(quant_ugraph.topo_order):
      op_info = quant_ugraph.ops_info[op_name]
      op_type = op_info.op_type
      # TODO: better abstraction for snippet
      if op_type == "Placeholder":
        parser = NamescopedKWArgsParser(RefCntOptimizer.KWARGS_NAMESCOPE, 
                                        op_info.op_attr)
        out_tname = op_info.output_tensors[0].name
        ref_count = parser.get('ref_counts', [0])[0]
        container.template_vars["placeholders"].append(out_tname)
        container.template_vars["ref_counts"].append(ref_count)
        header_snippet.template_vars["placeholders"].append(out_tname)
      else:
        # TODO: the operator may correspond to multiple snippets (such as InlinTensor)
        # weight_container is passed to function for workaround
        snippet = opFactory.createOperatorSnippet(op_info,
                                                  idx_dir=self.idx_dir,
                                                  embed_data_dir=self.embed_data_dir,
                                                  weight_container=weight_container,
                                                  data_manager=quant_ugraph.data_manager)
        container.add_snippet(snippet)

      if self.debug_cmt:
        comments = ["<<< Operation id {}: {}".format(op_id, op_name),
                    ">>> Operation id {}: {}".format(op_id + 1, op_name)]
        cmt_snippet = CommentSnippet(comments)
        container.add_snippet(cmt_snippet)
    composer.add_snippet(container)

    if any([method_name == 'inline' for method_name, _ in self.trans_methods]):  
      _logger.info("Generate weight file: %s", weightheader_fname)
      with open(weightheader_fname, "w") as wf:
        wf.write('// Auto generated by utensor-cli\n\n')
        wf.write(weight_container.render())
    else:
      container.remove_header('"{}"'.format(weightheader_name))
      
    _logger.info("Generate header file: %s", header_fname)
    with open(header_fname, "w") as wf:
      wf.write('// Auto generated by utensor-cli\n\n')
      wf.write(header_snippet.render())
    _logger.info("Generate source file: %s", src_fname)
    with open(src_fname, "w") as wf:
      wf.write('// Auto generated by utensor-cli\n\n')
      wf.write(composer.compose())
  
  @classmethod
  def _check_non_quantized(cls, ugraph):
    is_quantized = False
    for op_info in ugraph.ops_info.values():
      if op_info.op_type in [
        "Dequantize", "QuantizedMaxPool",
        "QuantizeV2", "QuantizedMatMul",
        "QuantizedRelu", "QuantizedAdd",
        "RequantizationRange",
        "Requantize",
        "QuantizedReshape",
        "QuantizedConv2D"
        ]:
        is_quantized = True
        break
    if is_quantized:
      _logger.warning(("Expecting non-quantized graph, "
                        "graph transformation/optimization might not work properly"))

  def _transform_graph(self, ugraph, methods):
    pipeline = TransformerPipeline(methods)
    return pipeline.transform(ugraph)

  def _tf_load_graph_def(self, pb_fname):
    with tf.gfile.FastGFile(pb_fname, 'rb') as fid:
      graph_def = tf.GraphDef()
      graph_def.ParseFromString(fid.read())
    return graph_def
