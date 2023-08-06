//
// Created by Dominik Krupke on 26.11.19.
//

#ifndef CGSHOP2020_VERIFIER_ISOLATED_VERTEX_CHECKER_H
#define CGSHOP2020_VERIFIER_ISOLATED_VERTEX_CHECKER_H
#include "base_checker.h"
namespace cgshop2020_verifier {
class LeafVertexChecker : public BaseChecker {
 public:

  std::unique_ptr<ErrorInformation> operator()(Instance &instance, Solution &solution) override
  {
    auto used_vertex_indices = this->collect_index_usage(solution);
    for (Instance::Index i = 0; i < instance.size(); ++i) {
      if (used_vertex_indices[i] == 1) {
        return std::make_unique<LeafVertexErrorInformation>(i);
      }
    }
    return {};
  }
 private:

  std::map<Instance::Index, int> collect_index_usage(const Solution &solution) const
  {
    std::map<Instance::Index, int> index_usage;
    for(uint64_t i=0; i<solution.size(); ++i){
      index_usage[i]=0;
    }
    for (const auto &edge: solution) {
      index_usage[edge.get_i()]+=1;
      index_usage[edge.get_j()]+=1;
    }
    return index_usage;
  }
};
}
#endif //CGSHOP2020_VERIFIER_ISOLATED_VERTEX_CHECKER_H
