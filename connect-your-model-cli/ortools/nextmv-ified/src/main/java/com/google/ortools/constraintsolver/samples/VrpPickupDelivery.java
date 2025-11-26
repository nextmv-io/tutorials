package com.google.ortools.constraintsolver.samples;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.google.ortools.Loader;
import com.google.ortools.constraintsolver.Assignment;
import com.google.ortools.constraintsolver.FirstSolutionStrategy;
import com.google.ortools.constraintsolver.RoutingDimension;
import com.google.ortools.constraintsolver.RoutingIndexManager;
import com.google.ortools.constraintsolver.RoutingModel;
import com.google.ortools.constraintsolver.RoutingSearchParameters;
import com.google.ortools.constraintsolver.Solver;
import com.google.ortools.constraintsolver.main;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Logger;

/** Minimal Pickup & Delivery Problem (PDP).*/
public class VrpPickupDelivery {
  private static final Logger logger = Logger.getLogger(VrpPickupDelivery.class.getName());

  static class DataModel {
    public long[][] distanceMatrix;
    public int[][] pickupsDeliveries;
    public int vehicleNumber;
    public int depot;

    public static DataModel loadFromFiles(String distanceFile, String pickupsDeliveriesFile, String problemFile) throws IOException {
      DataModel data = new DataModel();
      Gson gson = new Gson();

      // Load distance matrix
      try (FileReader reader = new FileReader(distanceFile)) {
        data.distanceMatrix = gson.fromJson(reader, long[][].class);
      }

      // Load pickups and deliveries
      try (FileReader reader = new FileReader(pickupsDeliveriesFile)) {
        data.pickupsDeliveries = gson.fromJson(reader, int[][].class);
      }

      // Load problem configuration
      try (FileReader reader = new FileReader(problemFile)) {
        JsonObject problemConfig = gson.fromJson(reader, JsonObject.class);
        data.vehicleNumber = problemConfig.get("vehicleNumber").getAsInt();
        data.depot = problemConfig.get("depot").getAsInt();
      }

      return data;
    }
  }

  static class Route {
    public int vehicle;
    public List<Integer> stops;
    public long distance;

    public Route(int vehicle, List<Integer> stops, long distance) {
      this.vehicle = vehicle;
      this.stops = stops;
      this.distance = distance;
    }
  }

  static class Solution {
    public List<Route> routes;

    public Solution(List<Route> routes) {
      this.routes = routes;
    }
  }

  static class SolutionOutput {
    public Solution solution;

    public SolutionOutput(Solution solution) {
      this.solution = solution;
    }
  }

  static class CustomStatistics {
    public double total_distance;
    public int total_routes;

    public CustomStatistics(double total_distance, int total_routes) {
      this.total_distance = total_distance;
      this.total_routes = total_routes;
    }
  }

  static class ResultStatistics {
    public double value;
    public double duration;
    public CustomStatistics custom;

    public ResultStatistics(double value, double duration, CustomStatistics custom) {
      this.value = value;
      this.duration = duration;
      this.custom = custom;
    }
  }

  static class Statistics {
    public String schema;
    public ResultStatistics result;

    public Statistics(String schema, ResultStatistics result) {
      this.schema = schema;
      this.result = result;
    }
  }

  static class StatisticsOutput {
    public Statistics statistics;

    public StatisticsOutput(Statistics statistics) {
      this.statistics = statistics;
    }
  }

  /// @brief Save the solution to a JSON file.
  static long saveSolutionToFile(
      DataModel data, RoutingModel routing, RoutingIndexManager manager, Assignment solution, String outputFile) throws IOException {
    List<Route> routes = new ArrayList<>();
    long totalDistance = 0;
    
    for (int i = 0; i < data.vehicleNumber; ++i) {
      if (!routing.isVehicleUsed(solution, i)) {
        continue;
      }
      
      List<Integer> stops = new ArrayList<>();
      long index = routing.start(i);
      long routeDistance = 0;
      
      while (!routing.isEnd(index)) {
        stops.add(manager.indexToNode(index));
        long previousIndex = index;
        index = solution.value(routing.nextVar(index));
        routeDistance += routing.getArcCostForVehicle(previousIndex, index, i);
      }
      stops.add(manager.indexToNode(index)); // Add final stop
      
      routes.add(new Route(i, stops, routeDistance));
      totalDistance += routeDistance;
    }
    
    Solution solutionData = new Solution(routes);
    SolutionOutput output = new SolutionOutput(solutionData);
    
    // Create output directory if it doesn't exist
    File file = new File(outputFile);
    file.getParentFile().mkdirs();
    
    // Write to JSON file
    Gson gson = new Gson();
    try (FileWriter writer = new FileWriter(outputFile)) {
      gson.toJson(output, writer);
    }
    
    logger.info("Solution saved to " + outputFile);
    return totalDistance;
  }

  /// @brief Save the statistics to a JSON file.
  static void saveStatisticsToFile(
      double objectiveValue, double durationSeconds, long totalDistance, int totalRoutes, String outputFile) throws IOException {
    CustomStatistics custom = new CustomStatistics(totalDistance, totalRoutes);
    ResultStatistics result = new ResultStatistics(objectiveValue, durationSeconds, custom);
    Statistics statistics = new Statistics("v1", result);
    StatisticsOutput output = new StatisticsOutput(statistics);
    
    // Create output directory if it doesn't exist
    File file = new File(outputFile);
    file.getParentFile().mkdirs();
    
    // Write to JSON file
    Gson gson = new Gson();
    try (FileWriter writer = new FileWriter(outputFile)) {
      gson.toJson(output, writer);
    }
    
    logger.info("Statistics saved to " + outputFile);
  }

  /// @brief Print the solution.
  static void printSolution(
      DataModel data, RoutingModel routing, RoutingIndexManager manager, Assignment solution) {
    // Solution cost.
    logger.info("Objective : " + solution.objectiveValue());
    // Inspect solution.
    long totalDistance = 0;
    for (int i = 0; i < data.vehicleNumber; ++i) {
      if (!routing.isVehicleUsed(solution, i)) {
        continue;
      }
      long index = routing.start(i);
      logger.info("Route for Vehicle " + i + ":");
      long routeDistance = 0;
      String route = "";
      while (!routing.isEnd(index)) {
        route += manager.indexToNode(index) + " -> ";
        long previousIndex = index;
        index = solution.value(routing.nextVar(index));
        routeDistance += routing.getArcCostForVehicle(previousIndex, index, i);
      }
      logger.info(route + manager.indexToNode(index));
      logger.info("Distance of the route: " + routeDistance + "m");
      totalDistance += routeDistance;
    }
    logger.info("Total Distance of all routes: " + totalDistance + "m");
  }

  public static void main(String[] args) throws Exception {
    Loader.loadNativeLibraries();
    
    // Parse command line arguments
    int vehicleMaximumTravelDistance = 3000; // default value
    int globalSpanCostCoefficient = 100; // default value
    for (int i = 0; i < args.length; i++) {
      if (args[i].equals("--vehicle_maximum_travel_distance") && i + 1 < args.length) {
        vehicleMaximumTravelDistance = Integer.parseInt(args[i + 1]);
      } else if (args[i].equals("--global_span_cost_coefficient") && i + 1 < args.length) {
        globalSpanCostCoefficient = Integer.parseInt(args[i + 1]);
      }
    }
    
    // Define input file paths
    String distanceFile = "inputs/distance.json";
    String pickupsDeliveriesFile = "inputs/pickups_deliveries.json";
    String problemFile = "inputs/problem.json";
    
    // Load the data from JSON files
    final DataModel data = DataModel.loadFromFiles(distanceFile, pickupsDeliveriesFile, problemFile);

    // Create Routing Index Manager
    RoutingIndexManager manager =
        new RoutingIndexManager(data.distanceMatrix.length, data.vehicleNumber, data.depot);

    // Create Routing Model.
    RoutingModel routing = new RoutingModel(manager);

    // Create and register a transit callback.
    final int transitCallbackIndex =
        routing.registerTransitCallback((long fromIndex, long toIndex) -> {
          // Convert from routing variable Index to user NodeIndex.
          int fromNode = manager.indexToNode(fromIndex);
          int toNode = manager.indexToNode(toIndex);
          return data.distanceMatrix[fromNode][toNode];
        });

    // Define cost of each arc.
    routing.setArcCostEvaluatorOfAllVehicles(transitCallbackIndex);

    // Add Distance constraint.
    boolean unused = routing.addDimension(transitCallbackIndex, // transit callback index
        0, // no slack
        vehicleMaximumTravelDistance, // vehicle maximum travel distance
        true, // start cumul to zero
        "Distance");
    RoutingDimension distanceDimension = routing.getMutableDimension("Distance");
    distanceDimension.setGlobalSpanCostCoefficient(globalSpanCostCoefficient);

    // Define Transportation Requests.
    Solver solver = routing.solver();
    for (int[] request : data.pickupsDeliveries) {
      long pickupIndex = manager.nodeToIndex(request[0]);
      long deliveryIndex = manager.nodeToIndex(request[1]);
      routing.addPickupAndDelivery(pickupIndex, deliveryIndex);
      solver.addConstraint(
          solver.makeEquality(routing.vehicleVar(pickupIndex), routing.vehicleVar(deliveryIndex)));
      solver.addConstraint(solver.makeLessOrEqual(
          distanceDimension.cumulVar(pickupIndex), distanceDimension.cumulVar(deliveryIndex)));
    }

    // Setting first solution heuristic.
    RoutingSearchParameters searchParameters =
        main.defaultRoutingSearchParameters()
            .toBuilder()
            .setFirstSolutionStrategy(FirstSolutionStrategy.Value.PARALLEL_CHEAPEST_INSERTION)
            .build();

    // Solve the problem and track duration.
    long startTime = System.nanoTime();
    Assignment solution = routing.solveWithParameters(searchParameters);
    long endTime = System.nanoTime();
    double durationSeconds = (endTime - startTime) / 1_000_000_000.0;

    // Print solution on console.
    printSolution(data, routing, manager, solution);
    
    // Save solution to JSON file and get total distance.
    String outputFile = "outputs/solutions/solution.json";
    long totalDistance = saveSolutionToFile(data, routing, manager, solution, outputFile);
    
    // Count total routes used.
    int totalRoutes = 0;
    for (int i = 0; i < data.vehicleNumber; ++i) {
      if (routing.isVehicleUsed(solution, i)) {
        totalRoutes++;
      }
    }
    
    // Save statistics to JSON file.
    String statisticsFile = "outputs/statistics/statistics.json";
    double objectiveValue = solution.objectiveValue();
    saveStatisticsToFile(objectiveValue, durationSeconds, totalDistance, totalRoutes, statisticsFile);
  }
}
