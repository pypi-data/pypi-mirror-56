//
// Created by Dominik Krupke on 26.11.19.
//

#include "catch.hpp"
#include <cgshop2020_verifier/full_checker.h>
using namespace cgshop2020_verifier;
TEST_CASE("Testing leaf vertex checker on some simple cases.", "[LeafVertexChecker]")
{
  SECTION("Square.") {

    Instance instance;
    instance.add_point(0.0, 0.0);
    instance.add_point(1.0, 0.0);
    instance.add_point(1.0, 1.0);
    instance.add_point(0.0, 1.0);
    instance.add_point(0.5, 0.5);

    Solution solution;
    solution.add_edge(0, 1);
    solution.add_edge(1, 2);
    solution.add_edge(2, 3);
    solution.add_edge(3, 0);
    solution.add_edge(0, 4);
    SolutionChecker checker;
    auto error = checker( /*instance=*/instance, /*solution=*/solution);
    bool is_error = error && error->is_error();
    REQUIRE(is_error);
    solution.add_edge(4, 2);
    error = checker( /*instance=*/instance, /*solution=*/solution);
    is_error = error && error->is_error();
    REQUIRE(!is_error);
  }
}

TEST_CASE("Testing circle leaf.", "[LeafVertexChecker]")
{
  SECTION("Square.") {

    Instance instance;
    instance.add_point(0.0, 0.0);
    instance.add_point(4.0, 0.0);
    instance.add_point(4.0, 4.0);
    instance.add_point(0.0, 4.0);

    instance.add_point(1.0, 1.0);
    instance.add_point(2.0, 1.0);
    instance.add_point(2.0, 2.0);
    instance.add_point(1.0, 2.0);


    Solution solution;
    solution.add_edge(0, 1);
    solution.add_edge(1, 2);
    solution.add_edge(2, 3);
    solution.add_edge(3, 0);
    solution.add_edge(4, 5);
    solution.add_edge(5, 6);
    solution.add_edge(6, 7);
    solution.add_edge(7, 4);

    solution.add_edge(0, 4);
    SolutionChecker checker;
    auto error = checker( /*instance=*/instance, /*solution=*/solution);
    bool is_error = error && error->is_error();
    REQUIRE(is_error);
    solution.add_edge(1, 5);
    solution.add_edge(2, 6);
    solution.add_edge(3, 7);
    error = checker( /*instance=*/instance, /*solution=*/solution);
    is_error = error && error->is_error();
    //std::cout << "ERRPOR"<<error->get_error_explanation() << std::endl;
    REQUIRE(!is_error);
  }
}