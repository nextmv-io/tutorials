// HiGHS is designed to solve linear optimization problems of the form
//
// Min (1/2)x^TQx + c^Tx + d subject to L <= Ax <= U; l <= x <= u
//
// where A is a matrix with m rows and n columns, and Q is either zero
// or positive definite. If Q is zero, HiGHS can determine the optimal
// integer-valued solution.
//
// The scalar n is num_col_
// The scalar m is num_row_
//
// The vector c is col_cost_
// The scalar d is offset_
// The vector l is col_lower_
// The vector u is col_upper_
// The vector L is row_lower_
// The vector U is row_upper_
//
// The matrix A is represented in packed vector form, either
// row-wise or column-wise: only its nonzeros are stored
//
// * The number of nonzeros in A is num_nz
//
// * The indices of the nonnzeros in the vectors of A are stored in a_index
//
// * The values of the nonnzeros in the vectors of A are stored in a_value
//
// * The position in a_index/a_value of the index/value of the first
// nonzero in each vector is stored in a_start
//
// Note that a_start[0] must be zero
//
// The matrix Q is represented in packed column form
//
// * The dimension of Q is dim_
//
// * The number of nonzeros in Q is hessian_num_nz
//
// * The indices of the nonnzeros in the vectors of A are stored in q_index
//
// * The values of the nonnzeros in the vectors of A are stored in q_value
//
// * The position in q_index/q_value of the index/value of the first
// nonzero in each column is stored in q_start
//
// Note
//
// * By default, Q is zero. This is indicated by dim_ being initialised to zero.
//
// * q_start[0] must be zero
//
#include <cassert>
#include <chrono>
#include <fstream>
#include <iostream>
#include <string>

#include "Highs.h"
#include "nlohmann/json.hpp"

#include <sstream>
#include <vector>

using std::cout;
using std::endl;
using json = nlohmann::json;

int main(int argc, char* argv[]) {
  // Start timing
  auto start_time = std::chrono::high_resolution_clock::now();
  
  // Parse command line arguments for time_limit
  double time_limit = 0.0;  // 0 means no limit
  for (int i = 1; i < argc; i++) {
    std::string arg = argv[i];
    if (arg.find("--time_limit=") == 0) {
      time_limit = std::stod(arg.substr(13));
    } else if (arg == "--time_limit" && i + 1 < argc) {
      time_limit = std::stod(argv[++i]);
    }
  }
  
  // Read and parse JSON from stdin
  json j;
  try {
    std::cin >> j;
  } catch (const json::parse_error& e) {
    std::cerr << "Error: Failed to parse JSON input: " << e.what() << std::endl;
    return 1;
  }
  
  if (j.empty()) {
    std::cerr << "Error: No input provided on stdin" << std::endl;
    return 1;
  }
  
  // Parse the JSON and create the model
  HighsModel model;
  model.lp_.num_col_ = j["num_col"].get<int>();
  model.lp_.num_row_ = j["num_row"].get<int>();
  model.lp_.sense_ = ObjSense::kMinimize;
  model.lp_.offset_ = j.value("offset", 0.0);
  model.lp_.col_cost_ = j["col_cost"].get<std::vector<double>>();
  model.lp_.col_lower_ = j["col_lower"].get<std::vector<double>>();
  model.lp_.col_upper_ = j["col_upper"].get<std::vector<double>>();
  model.lp_.row_lower_ = j["row_lower"].get<std::vector<double>>();
  model.lp_.row_upper_ = j["row_upper"].get<std::vector<double>>();
  
  // Parse the a_matrix object
  const auto& matrix = j["a_matrix"];
  
  // Set matrix format from JSON
  std::string format = matrix["format"].get<std::string>();
  if (format == "rowwise") {
    model.lp_.a_matrix_.format_ = MatrixFormat::kRowwise;
  } else {
    model.lp_.a_matrix_.format_ = MatrixFormat::kColwise;
  }
  model.lp_.a_matrix_.start_ = matrix["start"].get<std::vector<int>>();
  model.lp_.a_matrix_.index_ = matrix["index"].get<std::vector<int>>();
  model.lp_.a_matrix_.value_ = matrix["value"].get<std::vector<double>>();
  //
  // Create a Highs instance
  Highs highs;
  HighsStatus return_status;
  
  // Suppress HiGHS output
  highs.setOptionValue("output_flag", false);
  highs.setOptionValue("log_to_console", false);
  
  // Set time limit if provided
  if (time_limit > 0.0) {
    highs.setOptionValue("time_limit", time_limit);
    std::cerr << "Time limit set to " << time_limit << " seconds" << endl;
  }
  //
  // Pass the model to HiGHS
  return_status = highs.passModel(model);
  assert(return_status == HighsStatus::kOk);
  // If a user passes a model with entries in
  // model.lp_.a_matrix_.value_ less than (the option)
  // small_matrix_value in magnitude, they will be ignored. A logging
  // message will indicate this, and passModel will return
  // HighsStatus::kWarning
  //
  // Get a const reference to the LP data in HiGHS
  const HighsLp& lp = highs.getLp();
  //
  // Solve the model
  return_status = highs.run();
  assert(return_status == HighsStatus::kOk);
  //
  // Get the model status
  const HighsModelStatus& model_status = highs.getModelStatus();
  assert(model_status == HighsModelStatus::kOptimal);
  std::cerr << "Model status: " << highs.modelStatusToString(model_status) << endl;
  //
  // Get the solution information
  const HighsInfo& info = highs.getInfo();
  std::cerr << "Simplex iteration count: " << info.simplex_iteration_count << endl;
  std::cerr << "Objective function value: " << info.objective_function_value << endl;
  std::cerr << "Primal  solution status: "
       << highs.solutionStatusToString(info.primal_solution_status) << endl;
  std::cerr << "Dual    solution status: "
       << highs.solutionStatusToString(info.dual_solution_status) << endl;
  std::cerr << "Basis: " << highs.basisValidityToString(info.basis_validity) << endl;
  const bool has_values = info.primal_solution_status;
  const bool has_duals = info.dual_solution_status;
  const bool has_basis = info.basis_validity;
  //
  // Get the solution values and basis
  const HighsSolution& solution = highs.getSolution();
  const HighsBasis& basis = highs.getBasis();
  //
  // Report the primal and solution values and basis to stderr
  for (int col = 0; col < lp.num_col_; col++) {
    std::cerr << "Column " << col;
    if (has_values) std::cerr << "; value = " << solution.col_value[col];
    if (has_duals) std::cerr << "; dual = " << solution.col_dual[col];
    if (has_basis)
      std::cerr << "; status: " << highs.basisStatusToString(basis.col_status[col]);
    std::cerr << endl;
  }
  for (int row = 0; row < lp.num_row_; row++) {
    std::cerr << "Row    " << row;
    if (has_values) std::cerr << "; value = " << solution.row_value[row];
    if (has_duals) std::cerr << "; dual = " << solution.row_dual[row];
    if (has_basis)
      std::cerr << "; status: " << highs.basisStatusToString(basis.row_status[row]);
    std::cerr << endl;
  }

  // Now indicate that all the variables must take integer values from JSON
  if (j.contains("integrality")) {
    std::vector<int> integrality = j["integrality"].get<std::vector<int>>();
    if (!integrality.empty()) {
      model.lp_.integrality_.resize(lp.num_col_);
      for (int col = 0; col < lp.num_col_; col++)
        model.lp_.integrality_[col] = integrality[col] == 1 ? HighsVarType::kInteger : HighsVarType::kContinuous;
    }
  }

  highs.passModel(model);
  // Solve the model
  return_status = highs.run();
  assert(return_status == HighsStatus::kOk);
  
  // Calculate duration
  auto end_time = std::chrono::high_resolution_clock::now();
  std::chrono::duration<double> duration = end_time - start_time;
  
  // Build output JSON
  json output;
  
  // Add solution columns
  json columns = json::array();
  for (int col = 0; col < lp.num_col_; col++) {
    json column_obj;
    column_obj["index"] = col;
    if (info.primal_solution_status) {
      column_obj["value"] = solution.col_value[col];
    }
    columns.push_back(column_obj);
  }
  
  // Add solution rows
  json rows = json::array();
  for (int row = 0; row < lp.num_row_; row++) {
    json row_obj;
    row_obj["index"] = row;
    if (info.primal_solution_status) {
      row_obj["value"] = solution.row_value[row];
    }
    rows.push_back(row_obj);
  }
  
  // Build complete output structure
  output["solution"]["columns"] = columns;
  output["solution"]["rows"] = rows;
  output["statistics"]["schema"] = "v1";
  output["statistics"]["result"]["value"] = info.objective_function_value;
  output["statistics"]["result"]["duration"] = duration.count();
  output["statistics"]["result"]["custom"]["simplex_iteration_count"] = info.simplex_iteration_count;
  output["statistics"]["result"]["custom"]["status"] = highs.modelStatusToString(model_status);
  
  // Output formatted JSON to stdout
  cout << output.dump(2) << endl;

  highs.resetGlobalScheduler(true);

  return 0;
}
