# Vehicle Routing Problem

In the *Vehicle Routing Problem (VRP)*, the goal is to find optimal routes for
multiple vehicles visiting a set of locations. (When there's only one vehicle,
it reduces to the Traveling Salesperson Problem.)

But what do we mean by "optimal routes" for a VRP? One answer is the routes with
the least total distance. However, if there are no other constraints, the
optimal solution is to assign just one vehicle to visit all locations, and find
the shortest route for that vehicle. This is essentially the same problem as the
TSP.

A better way to define optimal routes is to minimize the length of the longest
single route among all vehicles. This is the right definition if the goal is to
complete all deliveries as soon as possible. The VRP example below finds optimal
routes defined this way.

In later sections, we'll describe other ways of generalizing the TSP by adding
constraints on the vehicles, including:

- [Capacity constraints](https://developers.google.com/optimization/routing/cvrp): the vehicles need to pick up items at each location they visit, but have a maximum carrying capacity.
- [Time windows](https://developers.google.com/optimization/routing/vrptw): each location must be visited within a specific time window.

## VRP example

This section presents an example of a VRP in which the goal is to minimize the
longest single route.

Imagine a company that needs to visit its customers in a city made up of
identical rectangular blocks.
A diagram of the city is shown below, with the company location marked in black
and the locations to visit in blue.

![](https://developers.google.com/static/optimization/images/routing/vrp.svg)

## Solving the VRP example with OR-Tools

The following sections explain how to solve the VRP example with OR-Tools.

### Create the data

The following function creates the data for the problem.  

### Python

```python
def create_data_model():
    """Stores the data for the problem."""
    data = {}
    data["distance_matrix"] = [
        # fmt: off
      [0, 548, 776, 696, 582, 274, 502, 194, 308, 194, 536, 502, 388, 354, 468, 776, 662],
      [548, 0, 684, 308, 194, 502, 730, 354, 696, 742, 1084, 594, 480, 674, 1016, 868, 1210],
      [776, 684, 0, 992, 878, 502, 274, 810, 468, 742, 400, 1278, 1164, 1130, 788, 1552, 754],
      [696, 308, 992, 0, 114, 650, 878, 502, 844, 890, 1232, 514, 628, 822, 1164, 560, 1358],
      [582, 194, 878, 114, 0, 536, 764, 388, 730, 776, 1118, 400, 514, 708, 1050, 674, 1244],
      [274, 502, 502, 650, 536, 0, 228, 308, 194, 240, 582, 776, 662, 628, 514, 1050, 708],
      [502, 730, 274, 878, 764, 228, 0, 536, 194, 468, 354, 1004, 890, 856, 514, 1278, 480],
      [194, 354, 810, 502, 388, 308, 536, 0, 342, 388, 730, 468, 354, 320, 662, 742, 856],
      [308, 696, 468, 844, 730, 194, 194, 342, 0, 274, 388, 810, 696, 662, 320, 1084, 514],
      [194, 742, 742, 890, 776, 240, 468, 388, 274, 0, 342, 536, 422, 388, 274, 810, 468],
      [536, 1084, 400, 1232, 1118, 582, 354, 730, 388, 342, 0, 878, 764, 730, 388, 1152, 354],
      [502, 594, 1278, 514, 400, 776, 1004, 468, 810, 536, 878, 0, 114, 308, 650, 274, 844],
      [388, 480, 1164, 628, 514, 662, 890, 354, 696, 422, 764, 114, 0, 194, 536, 388, 730],
      [354, 674, 1130, 822, 708, 628, 856, 320, 662, 388, 730, 308, 194, 0, 342, 422, 536],
      [468, 1016, 788, 1164, 1050, 514, 514, 662, 320, 274, 388, 650, 536, 342, 0, 764, 194],
      [776, 868, 1552, 560, 674, 1050, 1278, 742, 1084, 810, 1152, 274, 388, 422, 764, 0, 798],
      [662, 1210, 754, 1358, 1244, 708, 480, 856, 514, 468, 354, 844, 730, 536, 194, 798, 0],
        # fmt: on
    ]
    data["num_vehicles"] = 4
    data["depot"] = 0
    return data
```

### C++

```c++
struct DataModel {
  const std::vector<std::vector<int64_t>> distance_matrix{
      {0, 548, 776, 696, 582, 274, 502, 194, 308, 194, 536, 502, 388, 354, 468,
       776, 662},
      {548, 0, 684, 308, 194, 502, 730, 354, 696, 742, 1084, 594, 480, 674,
       1016, 868, 1210},
      {776, 684, 0, 992, 878, 502, 274, 810, 468, 742, 400, 1278, 1164, 1130,
       788, 1552, 754},
      {696, 308, 992, 0, 114, 650, 878, 502, 844, 890, 1232, 514, 628, 822,
       1164, 560, 1358},
      {582, 194, 878, 114, 0, 536, 764, 388, 730, 776, 1118, 400, 514, 708,
       1050, 674, 1244},
      {274, 502, 502, 650, 536, 0, 228, 308, 194, 240, 582, 776, 662, 628, 514,
       1050, 708},
      {502, 730, 274, 878, 764, 228, 0, 536, 194, 468, 354, 1004, 890, 856, 514,
       1278, 480},
      {194, 354, 810, 502, 388, 308, 536, 0, 342, 388, 730, 468, 354, 320, 662,
       742, 856},
      {308, 696, 468, 844, 730, 194, 194, 342, 0, 274, 388, 810, 696, 662, 320,
       1084, 514},
      {194, 742, 742, 890, 776, 240, 468, 388, 274, 0, 342, 536, 422, 388, 274,
       810, 468},
      {536, 1084, 400, 1232, 1118, 582, 354, 730, 388, 342, 0, 878, 764, 730,
       388, 1152, 354},
      {502, 594, 1278, 514, 400, 776, 1004, 468, 810, 536, 878, 0, 114, 308,
       650, 274, 844},
      {388, 480, 1164, 628, 514, 662, 890, 354, 696, 422, 764, 114, 0, 194, 536,
       388, 730},
      {354, 674, 1130, 822, 708, 628, 856, 320, 662, 388, 730, 308, 194, 0, 342,
       422, 536},
      {468, 1016, 788, 1164, 1050, 514, 514, 662, 320, 274, 388, 650, 536, 342,
       0, 764, 194},
      {776, 868, 1552, 560, 674, 1050, 1278, 742, 1084, 810, 1152, 274, 388,
       422, 764, 0, 798},
      {662, 1210, 754, 1358, 1244, 708, 480, 856, 514, 468, 354, 844, 730, 536,
       194, 798, 0},
  };
  const int num_vehicles = 4;
  const RoutingIndexManager::NodeIndex depot{0};
};
```

### Java

```java
static class DataModel {
  public final long[][] distanceMatrix = {
      {0, 548, 776, 696, 582, 274, 502, 194, 308, 194, 536, 502, 388, 354, 468, 776, 662},
      {548, 0, 684, 308, 194, 502, 730, 354, 696, 742, 1084, 594, 480, 674, 1016, 868, 1210},
      {776, 684, 0, 992, 878, 502, 274, 810, 468, 742, 400, 1278, 1164, 1130, 788, 1552, 754},
      {696, 308, 992, 0, 114, 650, 878, 502, 844, 890, 1232, 514, 628, 822, 1164, 560, 1358},
      {582, 194, 878, 114, 0, 536, 764, 388, 730, 776, 1118, 400, 514, 708, 1050, 674, 1244},
      {274, 502, 502, 650, 536, 0, 228, 308, 194, 240, 582, 776, 662, 628, 514, 1050, 708},
      {502, 730, 274, 878, 764, 228, 0, 536, 194, 468, 354, 1004, 890, 856, 514, 1278, 480},
      {194, 354, 810, 502, 388, 308, 536, 0, 342, 388, 730, 468, 354, 320, 662, 742, 856},
      {308, 696, 468, 844, 730, 194, 194, 342, 0, 274, 388, 810, 696, 662, 320, 1084, 514},
      {194, 742, 742, 890, 776, 240, 468, 388, 274, 0, 342, 536, 422, 388, 274, 810, 468},
      {536, 1084, 400, 1232, 1118, 582, 354, 730, 388, 342, 0, 878, 764, 730, 388, 1152, 354},
      {502, 594, 1278, 514, 400, 776, 1004, 468, 810, 536, 878, 0, 114, 308, 650, 274, 844},
      {388, 480, 1164, 628, 514, 662, 890, 354, 696, 422, 764, 114, 0, 194, 536, 388, 730},
      {354, 674, 1130, 822, 708, 628, 856, 320, 662, 388, 730, 308, 194, 0, 342, 422, 536},
      {468, 1016, 788, 1164, 1050, 514, 514, 662, 320, 274, 388, 650, 536, 342, 0, 764, 194},
      {776, 868, 1552, 560, 674, 1050, 1278, 742, 1084, 810, 1152, 274, 388, 422, 764, 0, 798},
      {662, 1210, 754, 1358, 1244, 708, 480, 856, 514, 468, 354, 844, 730, 536, 194, 798, 0},
  };
  public final int vehicleNumber = 4;
  public final int depot = 0;
}
```

### C#

```c#
class DataModel
{
    public long[,] DistanceMatrix = {
        { 0, 548, 776, 696, 582, 274, 502, 194, 308, 194, 536, 502, 388, 354, 468, 776, 662 },
        { 548, 0, 684, 308, 194, 502, 730, 354, 696, 742, 1084, 594, 480, 674, 1016, 868, 1210 },
        { 776, 684, 0, 992, 878, 502, 274, 810, 468, 742, 400, 1278, 1164, 1130, 788, 1552, 754 },
        { 696, 308, 992, 0, 114, 650, 878, 502, 844, 890, 1232, 514, 628, 822, 1164, 560, 1358 },
        { 582, 194, 878, 114, 0, 536, 764, 388, 730, 776, 1118, 400, 514, 708, 1050, 674, 1244 },
        { 274, 502, 502, 650, 536, 0, 228, 308, 194, 240, 582, 776, 662, 628, 514, 1050, 708 },
        { 502, 730, 274, 878, 764, 228, 0, 536, 194, 468, 354, 1004, 890, 856, 514, 1278, 480 },
        { 194, 354, 810, 502, 388, 308, 536, 0, 342, 388, 730, 468, 354, 320, 662, 742, 856 },
        { 308, 696, 468, 844, 730, 194, 194, 342, 0, 274, 388, 810, 696, 662, 320, 1084, 514 },
        { 194, 742, 742, 890, 776, 240, 468, 388, 274, 0, 342, 536, 422, 388, 274, 810, 468 },
        { 536, 1084, 400, 1232, 1118, 582, 354, 730, 388, 342, 0, 878, 764, 730, 388, 1152, 354 },
        { 502, 594, 1278, 514, 400, 776, 1004, 468, 810, 536, 878, 0, 114, 308, 650, 274, 844 },
        { 388, 480, 1164, 628, 514, 662, 890, 354, 696, 422, 764, 114, 0, 194, 536, 388, 730 },
        { 354, 674, 1130, 822, 708, 628, 856, 320, 662, 388, 730, 308, 194, 0, 342, 422, 536 },
        { 468, 1016, 788, 1164, 1050, 514, 514, 662, 320, 274, 388, 650, 536, 342, 0, 764, 194 },
        { 776, 868, 1552, 560, 674, 1050, 1278, 742, 1084, 810, 1152, 274, 388, 422, 764, 0, 798 },
        { 662, 1210, 754, 1358, 1244, 708, 480, 856, 514, 468, 354, 844, 730, 536, 194, 798, 0 }
    };
    public int VehicleNumber = 4;
    public int Depot = 0;
};
```

The data consists of:

- `distance_matrix`: An array of distances between locations on meters.
- `num_vehicles`: The number of vehicles in the fleet.
- `depot`: The index of the depot, the location where all vehicles start and end their routes.

### Location coordinates

To set up the example and compute the distance matrix, we have assigned the
following `x`-`y` coordinates to the locations shown in the
[city diagram](https://developers.google.com/optimization/routing/vrp#example):

<br />

```
[(456, 320), # location 0 - the depot
(228, 0),    # location 1
(912, 0),    # location 2
(0, 80),     # location 3
(114, 80),   # location 4
(570, 160),  # location 5
(798, 160),  # location 6
(342, 240),  # location 7
(684, 240),  # location 8
(570, 400),  # location 9
(912, 400),  # location 10
(114, 480),  # location 11
(228, 480),  # location 12
(342, 560),  # location 13
(684, 560),  # location 14
(0, 640),    # location 15
(798, 640)]  # location 16
```

<br />

Note that the location coordinates are not included in the problem data: all you
need to solve the problem is the distance matrix, which we have pre-computed.
You only need the location data to identify the locations in the solution, which
are denoted by their indices (0, 1, 2 ...) in the above list.

The main purpose of showing the location coordinates and the city diagram in
this and other examples is to provide a visual display of the problem and its
solution. But this is not essential for solving a VRP.

For convenience in setting up the problem, the distances between locations are
calculated using [Manhattan distance](https://en.wikipedia.org/wiki/Taxicab_geometry),
in which the distance between two points, (*x* ~1~, *y* ~1~)
and (*x* ~2~, *y* ~2~) is defined to be
\|*x* ~1~ - *x* ~2~\| + \|*y* ~1~ - *y* ~2~\|.
However, there is no special reason to use this definition. You can use whatever
method is best suited to your problem to calculate distances. Or, you can obtain
a distance matrix for any set of locations in the world using the Google
Distance Matrix API.
See [Distance Matrix API](https://developers.google.com/optimization/routing/vrp#distance_matrix_api) for an example of how to do this.

### Define the distance callback

As in the [TSP example](https://developers.google.com/optimization/routing/tsp#create_the_distance_callback),
the following function creates the distance callback, which returns the
distances between locations, and passes it to the solver. It also sets the arc
costs, which define the cost of travel, to be the distances of the arcs.  

### Python

```python
def distance_callback(from_index, to_index):
    """Returns the distance between the two nodes."""
    # Convert from routing variable Index to distance matrix NodeIndex.
    from_node = manager.IndexToNode(from_index)
    to_node = manager.IndexToNode(to_index)
    return data["distance_matrix"][from_node][to_node]

transit_callback_index = routing.RegisterTransitCallback(distance_callback)
routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
```

### C++

```c++
const int transit_callback_index = routing.RegisterTransitCallback(
    [&data, &manager](const int64_t from_index,
                      const int64_t to_index) -> int64_t {
      // Convert from routing variable Index to distance matrix NodeIndex.
      const int from_node = manager.IndexToNode(from_index).value();
      const int to_node = manager.IndexToNode(to_index).value();
      return data.distance_matrix[from_node][to_node];
    });
routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index);
```

### Java

```java
final int transitCallbackIndex =
    routing.registerTransitCallback((long fromIndex, long toIndex) -> {
      // Convert from routing variable Index to user NodeIndex.
      int fromNode = manager.indexToNode(fromIndex);
      int toNode = manager.indexToNode(toIndex);
      return data.distanceMatrix[fromNode][toNode];
    });
routing.setArcCostEvaluatorOfAllVehicles(transitCallbackIndex);
```

### C#

```c#
int transitCallbackIndex = routing.RegisterTransitCallback((long fromIndex, long toIndex) =>
                                                           {
                                                               // Convert from routing variable Index to
                                                               // distance matrix NodeIndex.
                                                               var fromNode = manager.IndexToNode(fromIndex);
                                                               var toNode = manager.IndexToNode(toIndex);
                                                               return data.DistanceMatrix[fromNode, toNode];
                                                           });
routing.SetArcCostEvaluatorOfAllVehicles(transitCallbackIndex);
```

### Add a distance dimension

To solve this VRP, you need to create a distance **dimension** , which computes
the cumulative distance traveled by each vehicle along its route. You can then
set a cost proportional to the maximum of the total distances along each route.
Routing programs use dimensions to keep track of quantities that accumulate over
a vehicle's route.
See [Dimensions](https://developers.google.com/optimization/routing/dimensions) for more details.

The following code creates the distance dimension, using the solver's
[`AddDimension`](https://developers.google.com/optimization/reference/constraint_solver/routing/RoutingModel#AddDimension)
method. The argument `transit_callback_index` is the index for the
[distance_callback](https://developers.google.com/optimization/routing/vrp#define_the_distance_callback).  

### Python

```python
dimension_name = "Distance"
routing.AddDimension(
    transit_callback_index,
    0,  # no slack
    3000,  # vehicle maximum travel distance
    True,  # start cumul to zero
    dimension_name,
)
distance_dimension = routing.GetDimensionOrDie(dimension_name)
distance_dimension.SetGlobalSpanCostCoefficient(100)
```

### C++

```c++
routing.AddDimension(transit_callback_index, 0, 3000,
                     true,  // start cumul to zero
                     "Distance");
routing.GetMutableDimension("Distance")->SetGlobalSpanCostCoefficient(100);
```

### Java

```java
boolean unused = routing.addDimension(transitCallbackIndex, 0, 3000,
    true, // start cumul to zero
    "Distance");
RoutingDimension distanceDimension = routing.getMutableDimension("Distance");
distanceDimension.setGlobalSpanCostCoefficient(100);
```

### C#

```c#
routing.AddDimension(transitCallbackIndex, 0, 3000,
                     true, // start cumul to zero
                     "Distance");
RoutingDimension distanceDimension = routing.GetMutableDimension("Distance");
distanceDimension.SetGlobalSpanCostCoefficient(100);
```

The method `SetGlobalSpanCostCoefficient` sets a large coefficient (`100`) for
the **global span** of the routes, which in this example is the maximum of the
distances of the routes. This makes the global span the predominant factor in
the objective function, so the program minimizes the length of the longest route.

### Add the solution printer

The function that prints the solution is shown below.  

### Python

```python
def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f"Objective: {solution.ObjectiveValue()}")
    max_route_distance = 0
    for vehicle_id in range(data["num_vehicles"]):
        if not routing.IsVehicleUsed(solution, vehicle_id):
            continue
        index = routing.Start(vehicle_id)
        plan_output = f"Route for vehicle {vehicle_id}:\n"
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += f" {manager.IndexToNode(index)} -> "
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id
            )
        plan_output += f"{manager.IndexToNode(index)}\n"
        plan_output += f"Distance of the route: {route_distance}m\n"
        print(plan_output)
        max_route_distance = max(route_distance, max_route_distance)
    print(f"Maximum of the route distances: {max_route_distance}m")
```

### C++

```c++
void PrintSolution(const DataModel& data, const RoutingIndexManager& manager,
                   const RoutingModel& routing, const Assignment& solution) {
  int64_t max_route_distance{0};
  for (int vehicle_id = 0; vehicle_id < data.num_vehicles; ++vehicle_id) {
    if (!routing.IsVehicleUsed(solution, vehicle_id)) {
      continue;
    }
    int64_t index = routing.Start(vehicle_id);
    LOG(INFO) << "Route for Vehicle " << vehicle_id << ":";
    int64_t route_distance{0};
    std::stringstream route;
    while (!routing.IsEnd(index)) {
      route << manager.IndexToNode(index).value() << " -> ";
      const int64_t previous_index = index;
      index = solution.Value(routing.NextVar(index));
      route_distance += routing.GetArcCostForVehicle(previous_index, index,
                                                     int64_t{vehicle_id});
    }
    LOG(INFO) << route.str() << manager.IndexToNode(index).value();
    LOG(INFO) << "Distance of the route: " << route_distance << "m";
    max_route_distance = std::max(route_distance, max_route_distance);
  }
  LOG(INFO) << "Maximum of the route distances: " << max_route_distance << "m";
  LOG(INFO) << "";
  LOG(INFO) << "Problem solved in " << routing.solver()->wall_time() << "ms";
}
```

### Java

```java
/// @brief Print the solution.
static void printSolution(
    DataModel data, RoutingModel routing, RoutingIndexManager manager, Assignment solution) {
  // Solution cost.
  logger.info("Objective : " + solution.objectiveValue());
  // Inspect solution.
  long maxRouteDistance = 0;
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
    maxRouteDistance = Math.max(routeDistance, maxRouteDistance);
  }
  logger.info("Maximum of the route distances: " + maxRouteDistance + "m");
}
```

### C#

```c#
/// <summary>
///   Print the solution.
/// </summary>
static void PrintSolution(in DataModel data, in RoutingModel routing, in RoutingIndexManager manager,
                          in Assignment solution)
{
    Console.WriteLine($"Objective {solution.ObjectiveValue()}:");

    // Inspect solution.
    long maxRouteDistance = 0;
    for (int i = 0; i < data.VehicleNumber; ++i)
    {
        if (!routing.IsVehicleUsed(solution, i))
        {
            continue;
        }
        Console.WriteLine("Route for Vehicle {0}:", i);
        long routeDistance = 0;
        var index = routing.Start(i);
        while (routing.IsEnd(index) == false)
        {
            Console.Write("{0} -> ", manager.IndexToNode((int)index));
            var previousIndex = index;
            index = solution.Value(routing.NextVar(index));
            routeDistance += routing.GetArcCostForVehicle(previousIndex, index, 0);
        }
        Console.WriteLine("{0}", manager.IndexToNode((int)index));
        Console.WriteLine("Distance of the route: {0}m", routeDistance);
        maxRouteDistance = Math.Max(routeDistance, maxRouteDistance);
    }
    Console.WriteLine("Maximum distance of the routes: {0}m", maxRouteDistance);
}
```

The function displays the routes for the vehicles and the total distances of the
routes.

Alternatively, you can first
[save the routes](https://developers.google.com/optimization/routing/tsp#get-routes) to a list or array, and
then print them.

### Main function

Most of the code in the main function for the VRP program is the same as in the
previous TSP example. See the [TSP section](https://developers.google.com/optimization/routing/tsp#create_model)
for a description of that code. What's new is the
[distance dimension](https://developers.google.com/optimization/routing/vrp#add_a_distance_dimension), described above.

### Running the programs

The complete programs are shown in the [next section](https://developers.google.com/optimization/routing/vrp#complete_programs).
When you run the programs, they display the following output:  

```
Objective: 177500
Route for vehicle 0:
 0 ->  9 ->  10 ->  2 ->  6 ->  5 -> 0
Distance of the route: 1712m

Route for vehicle 1:
 0 ->  16 ->  14 ->  8 -> 0
Distance of the route: 1484m

Route for vehicle 2:
 0 ->  7 ->  1 ->  4 ->  3 -> 0
Distance of the route: 1552m

Route for vehicle 3:
 0 ->  13 ->  15 ->  11 ->  12 -> 0
Distance of the route: 1552m

Maximum of the route distances: 1712m
```

The locations in the routes are denoted by their indices in the
[locations list](https://developers.google.com/optimization/routing/vrp#manhattan_distance). All routes begin and end at the depot
(`0`).

The diagram below shows the assigned routes, in which the location indices have
been converted to the corresponding `x`-`y` coordinates.

![](https://developers.google.com/static/optimization/images/routing/vrpgs_solution.svg)

### Complete programs

The complete programs that minimizes the longest single route are shown below.  

### Python

```python
"""Simple Vehicles Routing Problem (VRP).

This is a sample using the routing library python wrapper to solve a VRP
problem.
A description of the problem can be found here:
http://en.wikipedia.org/wiki/Vehicle_routing_problem.

Distances are in meters.
"""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp



def create_data_model():
    """Stores the data for the problem."""
    data = {}
    data["distance_matrix"] = [
        # fmt: off
      [0, 548, 776, 696, 582, 274, 502, 194, 308, 194, 536, 502, 388, 354, 468, 776, 662],
      [548, 0, 684, 308, 194, 502, 730, 354, 696, 742, 1084, 594, 480, 674, 1016, 868, 1210],
      [776, 684, 0, 992, 878, 502, 274, 810, 468, 742, 400, 1278, 1164, 1130, 788, 1552, 754],
      [696, 308, 992, 0, 114, 650, 878, 502, 844, 890, 1232, 514, 628, 822, 1164, 560, 1358],
      [582, 194, 878, 114, 0, 536, 764, 388, 730, 776, 1118, 400, 514, 708, 1050, 674, 1244],
      [274, 502, 502, 650, 536, 0, 228, 308, 194, 240, 582, 776, 662, 628, 514, 1050, 708],
      [502, 730, 274, 878, 764, 228, 0, 536, 194, 468, 354, 1004, 890, 856, 514, 1278, 480],
      [194, 354, 810, 502, 388, 308, 536, 0, 342, 388, 730, 468, 354, 320, 662, 742, 856],
      [308, 696, 468, 844, 730, 194, 194, 342, 0, 274, 388, 810, 696, 662, 320, 1084, 514],
      [194, 742, 742, 890, 776, 240, 468, 388, 274, 0, 342, 536, 422, 388, 274, 810, 468],
      [536, 1084, 400, 1232, 1118, 582, 354, 730, 388, 342, 0, 878, 764, 730, 388, 1152, 354],
      [502, 594, 1278, 514, 400, 776, 1004, 468, 810, 536, 878, 0, 114, 308, 650, 274, 844],
      [388, 480, 1164, 628, 514, 662, 890, 354, 696, 422, 764, 114, 0, 194, 536, 388, 730],
      [354, 674, 1130, 822, 708, 628, 856, 320, 662, 388, 730, 308, 194, 0, 342, 422, 536],
      [468, 1016, 788, 1164, 1050, 514, 514, 662, 320, 274, 388, 650, 536, 342, 0, 764, 194],
      [776, 868, 1552, 560, 674, 1050, 1278, 742, 1084, 810, 1152, 274, 388, 422, 764, 0, 798],
      [662, 1210, 754, 1358, 1244, 708, 480, 856, 514, 468, 354, 844, 730, 536, 194, 798, 0],
        # fmt: on
    ]
    data["num_vehicles"] = 4
    data["depot"] = 0
    return data


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f"Objective: {solution.ObjectiveValue()}")
    max_route_distance = 0
    for vehicle_id in range(data["num_vehicles"]):
        if not routing.IsVehicleUsed(solution, vehicle_id):
            continue
        index = routing.Start(vehicle_id)
        plan_output = f"Route for vehicle {vehicle_id}:\n"
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += f" {manager.IndexToNode(index)} -> "
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id
            )
        plan_output += f"{manager.IndexToNode(index)}\n"
        plan_output += f"Distance of the route: {route_distance}m\n"
        print(plan_output)
        max_route_distance = max(route_distance, max_route_distance)
    print(f"Maximum of the route distances: {max_route_distance}m")



def main():
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = "Distance"
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        3000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name,
    )
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)
    else:
        print("No solution found !")


if __name__ == "__main__":
    main()
```

### C++

```c++
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <sstream>
#include <vector>

#include "ortools/base/logging.h"
#include "ortools/constraint_solver/constraint_solver.h"
#include "ortools/constraint_solver/routing.h"
#include "ortools/constraint_solver/routing_enums.pb.h"
#include "ortools/constraint_solver/routing_index_manager.h"
#include "ortools/constraint_solver/routing_parameters.h"

namespace operations_research {
struct DataModel {
  const std::vector<std::vector<int64_t>> distance_matrix{
      {0, 548, 776, 696, 582, 274, 502, 194, 308, 194, 536, 502, 388, 354, 468,
       776, 662},
      {548, 0, 684, 308, 194, 502, 730, 354, 696, 742, 1084, 594, 480, 674,
       1016, 868, 1210},
      {776, 684, 0, 992, 878, 502, 274, 810, 468, 742, 400, 1278, 1164, 1130,
       788, 1552, 754},
      {696, 308, 992, 0, 114, 650, 878, 502, 844, 890, 1232, 514, 628, 822,
       1164, 560, 1358},
      {582, 194, 878, 114, 0, 536, 764, 388, 730, 776, 1118, 400, 514, 708,
       1050, 674, 1244},
      {274, 502, 502, 650, 536, 0, 228, 308, 194, 240, 582, 776, 662, 628, 514,
       1050, 708},
      {502, 730, 274, 878, 764, 228, 0, 536, 194, 468, 354, 1004, 890, 856, 514,
       1278, 480},
      {194, 354, 810, 502, 388, 308, 536, 0, 342, 388, 730, 468, 354, 320, 662,
       742, 856},
      {308, 696, 468, 844, 730, 194, 194, 342, 0, 274, 388, 810, 696, 662, 320,
       1084, 514},
      {194, 742, 742, 890, 776, 240, 468, 388, 274, 0, 342, 536, 422, 388, 274,
       810, 468},
      {536, 1084, 400, 1232, 1118, 582, 354, 730, 388, 342, 0, 878, 764, 730,
       388, 1152, 354},
      {502, 594, 1278, 514, 400, 776, 1004, 468, 810, 536, 878, 0, 114, 308,
       650, 274, 844},
      {388, 480, 1164, 628, 514, 662, 890, 354, 696, 422, 764, 114, 0, 194, 536,
       388, 730},
      {354, 674, 1130, 822, 708, 628, 856, 320, 662, 388, 730, 308, 194, 0, 342,
       422, 536},
      {468, 1016, 788, 1164, 1050, 514, 514, 662, 320, 274, 388, 650, 536, 342,
       0, 764, 194},
      {776, 868, 1552, 560, 674, 1050, 1278, 742, 1084, 810, 1152, 274, 388,
       422, 764, 0, 798},
      {662, 1210, 754, 1358, 1244, 708, 480, 856, 514, 468, 354, 844, 730, 536,
       194, 798, 0},
  };
  const int num_vehicles = 4;
  const RoutingIndexManager::NodeIndex depot{0};
};

//! @brief Print the solution.
//! @param[in] data Data of the problem.
//! @param[in] manager Index manager used.
//! @param[in] routing Routing solver used.
//! @param[in] solution Solution found by the solver.
void PrintSolution(const DataModel& data, const RoutingIndexManager& manager,
                   const RoutingModel& routing, const Assignment& solution) {
  int64_t max_route_distance{0};
  for (int vehicle_id = 0; vehicle_id < data.num_vehicles; ++vehicle_id) {
    if (!routing.IsVehicleUsed(solution, vehicle_id)) {
      continue;
    }
    int64_t index = routing.Start(vehicle_id);
    LOG(INFO) << "Route for Vehicle " << vehicle_id << ":";
    int64_t route_distance{0};
    std::stringstream route;
    while (!routing.IsEnd(index)) {
      route << manager.IndexToNode(index).value() << " -> ";
      const int64_t previous_index = index;
      index = solution.Value(routing.NextVar(index));
      route_distance += routing.GetArcCostForVehicle(previous_index, index,
                                                     int64_t{vehicle_id});
    }
    LOG(INFO) << route.str() << manager.IndexToNode(index).value();
    LOG(INFO) << "Distance of the route: " << route_distance << "m";
    max_route_distance = std::max(route_distance, max_route_distance);
  }
  LOG(INFO) << "Maximum of the route distances: " << max_route_distance << "m";
  LOG(INFO) << "";
  LOG(INFO) << "Problem solved in " << routing.solver()->wall_time() << "ms";
}

void VrpGlobalSpan() {
  // Instantiate the data problem.
  DataModel data;

  // Create Routing Index Manager
  RoutingIndexManager manager(data.distance_matrix.size(), data.num_vehicles,
                              data.depot);

  // Create Routing Model.
  RoutingModel routing(manager);

  // Create and register a transit callback.
  const int transit_callback_index = routing.RegisterTransitCallback(
      [&data, &manager](const int64_t from_index,
                        const int64_t to_index) -> int64_t {
        // Convert from routing variable Index to distance matrix NodeIndex.
        const int from_node = manager.IndexToNode(from_index).value();
        const int to_node = manager.IndexToNode(to_index).value();
        return data.distance_matrix[from_node][to_node];
      });

  // Define cost of each arc.
  routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index);

  // Add Distance constraint.
  routing.AddDimension(transit_callback_index, 0, 3000,
                       true,  // start cumul to zero
                       "Distance");
  routing.GetMutableDimension("Distance")->SetGlobalSpanCostCoefficient(100);

  // Setting first solution heuristic.
  RoutingSearchParameters searchParameters = DefaultRoutingSearchParameters();
  searchParameters.set_first_solution_strategy(
      FirstSolutionStrategy::PATH_CHEAPEST_ARC);

  // Solve the problem.
  const Assignment* solution = routing.SolveWithParameters(searchParameters);

  // Print solution on console.
  if (solution != nullptr) {
    PrintSolution(data, manager, routing, *solution);
  } else {
    LOG(INFO) << "No solution found.";
  }
}
}  // namespace operations_research

int main(int /*argc*/, char* /*argv*/[]) {
  operations_research::VrpGlobalSpan();
  return EXIT_SUCCESS;
}
```

### Java

```java
package com.google.ortools.constraintsolver.samples;

import com.google.ortools.Loader;
import com.google.ortools.constraintsolver.Assignment;
import com.google.ortools.constraintsolver.FirstSolutionStrategy;
import com.google.ortools.constraintsolver.RoutingDimension;
import com.google.ortools.constraintsolver.RoutingIndexManager;
import com.google.ortools.constraintsolver.RoutingModel;
import com.google.ortools.constraintsolver.RoutingSearchParameters;
import com.google.ortools.constraintsolver.main;
import java.util.logging.Logger;

/** Minimal VRP.*/
public class VrpGlobalSpan {
  private static final Logger logger = Logger.getLogger(VrpGlobalSpan.class.getName());

  static class DataModel {
    public final long[][] distanceMatrix = {
        {0, 548, 776, 696, 582, 274, 502, 194, 308, 194, 536, 502, 388, 354, 468, 776, 662},
        {548, 0, 684, 308, 194, 502, 730, 354, 696, 742, 1084, 594, 480, 674, 1016, 868, 1210},
        {776, 684, 0, 992, 878, 502, 274, 810, 468, 742, 400, 1278, 1164, 1130, 788, 1552, 754},
        {696, 308, 992, 0, 114, 650, 878, 502, 844, 890, 1232, 514, 628, 822, 1164, 560, 1358},
        {582, 194, 878, 114, 0, 536, 764, 388, 730, 776, 1118, 400, 514, 708, 1050, 674, 1244},
        {274, 502, 502, 650, 536, 0, 228, 308, 194, 240, 582, 776, 662, 628, 514, 1050, 708},
        {502, 730, 274, 878, 764, 228, 0, 536, 194, 468, 354, 1004, 890, 856, 514, 1278, 480},
        {194, 354, 810, 502, 388, 308, 536, 0, 342, 388, 730, 468, 354, 320, 662, 742, 856},
        {308, 696, 468, 844, 730, 194, 194, 342, 0, 274, 388, 810, 696, 662, 320, 1084, 514},
        {194, 742, 742, 890, 776, 240, 468, 388, 274, 0, 342, 536, 422, 388, 274, 810, 468},
        {536, 1084, 400, 1232, 1118, 582, 354, 730, 388, 342, 0, 878, 764, 730, 388, 1152, 354},
        {502, 594, 1278, 514, 400, 776, 1004, 468, 810, 536, 878, 0, 114, 308, 650, 274, 844},
        {388, 480, 1164, 628, 514, 662, 890, 354, 696, 422, 764, 114, 0, 194, 536, 388, 730},
        {354, 674, 1130, 822, 708, 628, 856, 320, 662, 388, 730, 308, 194, 0, 342, 422, 536},
        {468, 1016, 788, 1164, 1050, 514, 514, 662, 320, 274, 388, 650, 536, 342, 0, 764, 194},
        {776, 868, 1552, 560, 674, 1050, 1278, 742, 1084, 810, 1152, 274, 388, 422, 764, 0, 798},
        {662, 1210, 754, 1358, 1244, 708, 480, 856, 514, 468, 354, 844, 730, 536, 194, 798, 0},
    };
    public final int vehicleNumber = 4;
    public final int depot = 0;
  }

  /// @brief Print the solution.
  static void printSolution(
      DataModel data, RoutingModel routing, RoutingIndexManager manager, Assignment solution) {
    // Solution cost.
    logger.info("Objective : " + solution.objectiveValue());
    // Inspect solution.
    long maxRouteDistance = 0;
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
      maxRouteDistance = Math.max(routeDistance, maxRouteDistance);
    }
    logger.info("Maximum of the route distances: " + maxRouteDistance + "m");
  }

  public static void main(String[] args) throws Exception {
    Loader.loadNativeLibraries();
    // Instantiate the data problem.
    final DataModel data = new DataModel();

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
    boolean unused = routing.addDimension(transitCallbackIndex, 0, 3000,
        true, // start cumul to zero
        "Distance");
    RoutingDimension distanceDimension = routing.getMutableDimension("Distance");
    distanceDimension.setGlobalSpanCostCoefficient(100);

    // Setting first solution heuristic.
    RoutingSearchParameters searchParameters =
        main.defaultRoutingSearchParameters()
            .toBuilder()
            .setFirstSolutionStrategy(FirstSolutionStrategy.Value.PATH_CHEAPEST_ARC)
            .build();

    // Solve the problem.
    Assignment solution = routing.solveWithParameters(searchParameters);

    // Print solution on console.
    printSolution(data, routing, manager, solution);
  }
}
```

### C#

```c#
using System;
using System.Collections.Generic;
using Google.OrTools.ConstraintSolver;

/// <summary>
///   Minimal TSP using distance matrix.
/// </summary>
public class VrpGlobalSpan
{
    class DataModel
    {
        public long[,] DistanceMatrix = {
            { 0, 548, 776, 696, 582, 274, 502, 194, 308, 194, 536, 502, 388, 354, 468, 776, 662 },
            { 548, 0, 684, 308, 194, 502, 730, 354, 696, 742, 1084, 594, 480, 674, 1016, 868, 1210 },
            { 776, 684, 0, 992, 878, 502, 274, 810, 468, 742, 400, 1278, 1164, 1130, 788, 1552, 754 },
            { 696, 308, 992, 0, 114, 650, 878, 502, 844, 890, 1232, 514, 628, 822, 1164, 560, 1358 },
            { 582, 194, 878, 114, 0, 536, 764, 388, 730, 776, 1118, 400, 514, 708, 1050, 674, 1244 },
            { 274, 502, 502, 650, 536, 0, 228, 308, 194, 240, 582, 776, 662, 628, 514, 1050, 708 },
            { 502, 730, 274, 878, 764, 228, 0, 536, 194, 468, 354, 1004, 890, 856, 514, 1278, 480 },
            { 194, 354, 810, 502, 388, 308, 536, 0, 342, 388, 730, 468, 354, 320, 662, 742, 856 },
            { 308, 696, 468, 844, 730, 194, 194, 342, 0, 274, 388, 810, 696, 662, 320, 1084, 514 },
            { 194, 742, 742, 890, 776, 240, 468, 388, 274, 0, 342, 536, 422, 388, 274, 810, 468 },
            { 536, 1084, 400, 1232, 1118, 582, 354, 730, 388, 342, 0, 878, 764, 730, 388, 1152, 354 },
            { 502, 594, 1278, 514, 400, 776, 1004, 468, 810, 536, 878, 0, 114, 308, 650, 274, 844 },
            { 388, 480, 1164, 628, 514, 662, 890, 354, 696, 422, 764, 114, 0, 194, 536, 388, 730 },
            { 354, 674, 1130, 822, 708, 628, 856, 320, 662, 388, 730, 308, 194, 0, 342, 422, 536 },
            { 468, 1016, 788, 1164, 1050, 514, 514, 662, 320, 274, 388, 650, 536, 342, 0, 764, 194 },
            { 776, 868, 1552, 560, 674, 1050, 1278, 742, 1084, 810, 1152, 274, 388, 422, 764, 0, 798 },
            { 662, 1210, 754, 1358, 1244, 708, 480, 856, 514, 468, 354, 844, 730, 536, 194, 798, 0 }
        };
        public int VehicleNumber = 4;
        public int Depot = 0;
    };

    /// <summary>
    ///   Print the solution.
    /// </summary>
    static void PrintSolution(in DataModel data, in RoutingModel routing, in RoutingIndexManager manager,
                              in Assignment solution)
    {
        Console.WriteLine($"Objective {solution.ObjectiveValue()}:");

        // Inspect solution.
        long maxRouteDistance = 0;
        for (int i = 0; i < data.VehicleNumber; ++i)
        {
            if (!routing.IsVehicleUsed(solution, i))
            {
                continue;
            }
            Console.WriteLine("Route for Vehicle {0}:", i);
            long routeDistance = 0;
            var index = routing.Start(i);
            while (routing.IsEnd(index) == false)
            {
                Console.Write("{0} -> ", manager.IndexToNode((int)index));
                var previousIndex = index;
                index = solution.Value(routing.NextVar(index));
                routeDistance += routing.GetArcCostForVehicle(previousIndex, index, 0);
            }
            Console.WriteLine("{0}", manager.IndexToNode((int)index));
            Console.WriteLine("Distance of the route: {0}m", routeDistance);
            maxRouteDistance = Math.Max(routeDistance, maxRouteDistance);
        }
        Console.WriteLine("Maximum distance of the routes: {0}m", maxRouteDistance);
    }

    public static void Main(String[] args)
    {
        // Instantiate the data problem.
        DataModel data = new DataModel();

        // Create Routing Index Manager
        RoutingIndexManager manager =
            new RoutingIndexManager(data.DistanceMatrix.GetLength(0), data.VehicleNumber, data.Depot);


        // Create Routing Model.
        RoutingModel routing = new RoutingModel(manager);

        // Create and register a transit callback.
        int transitCallbackIndex = routing.RegisterTransitCallback((long fromIndex, long toIndex) =>
                                                                   {
                                                                       // Convert from routing variable Index to
                                                                       // distance matrix NodeIndex.
                                                                       var fromNode = manager.IndexToNode(fromIndex);
                                                                       var toNode = manager.IndexToNode(toIndex);
                                                                       return data.DistanceMatrix[fromNode, toNode];
                                                                   });

        // Define cost of each arc.
        routing.SetArcCostEvaluatorOfAllVehicles(transitCallbackIndex);

        // Add Distance constraint.
        routing.AddDimension(transitCallbackIndex, 0, 3000,
                             true, // start cumul to zero
                             "Distance");
        RoutingDimension distanceDimension = routing.GetMutableDimension("Distance");
        distanceDimension.SetGlobalSpanCostCoefficient(100);

        // Setting first solution heuristic.
        RoutingSearchParameters searchParameters =
            operations_research_constraint_solver.DefaultRoutingSearchParameters();
        searchParameters.FirstSolutionStrategy = FirstSolutionStrategy.Types.Value.PathCheapestArc;

        // Solve the problem.
        Assignment solution = routing.SolveWithParameters(searchParameters);

        // Print solution on console.
        PrintSolution(data, routing, manager, solution);
    }
}
```

## Using the Google Distance Matrix API

The section shows how to use the
[Google Distance Matrix API](https://developers.google.com/maps/documentation/distance-matrix/start)
to create the distance matrix for any set of locations defined by addresses, or
by latitudes and longitudes. You can use the API to calculate the distance
matrix for many types of routing problems.

To use the API, you'll need an API key. Here's how to
[obtain one](https://developers.google.com/maps/documentation/distance-matrix/start#get-a-key).

### Example

As an example, we'll walk through a Python program that creates the distance
matrix for a set of 16 locations in the city of Memphis, Tennessee.
The distance matrix is a 16 x 16 matrix whose `i`, `j` entry is the
distance between locations `i` and `j`. Here are the addresses for the locations.  

```python
data['addresses'] = ['3610+Hacks+Cross+Rd+Memphis+TN', # depot
                     '1921+Elvis+Presley+Blvd+Memphis+TN',
                     '149+Union+Avenue+Memphis+TN',
                     '1034+Audubon+Drive+Memphis+TN',
                     '1532+Madison+Ave+Memphis+TN',
                     '706+Union+Ave+Memphis+TN',
                     '3641+Central+Ave+Memphis+TN',
                     '926+E+McLemore+Ave+Memphis+TN',
                     '4339+Park+Ave+Memphis+TN',
                     '600+Goodwyn+St+Memphis+TN',
                     '2000+North+Pkwy+Memphis+TN',
                     '262+Danny+Thomas+Pl+Memphis+TN',
                     '125+N+Front+St+Memphis+TN',
                     '5959+Park+Ave+Memphis+TN',
                     '814+Scott+St+Memphis+TN',
                     '1005+Tillman+St+Memphis+TN'
                    ]
```

### API requests

A Distance Matrix API request is a long string containing the following:

- API address: `https://maps.googleapis.com/maps/api/distancematrix/json?`. The end of the request, `json`, asks for the response in JSON.
- Request options. In this example, `units=imperial` sets the language of the response to English.
- Origin addresses: Travel starting points. For example `&origins=3610+Hacks+Cross+Rd+Memphis+TN`.  
  Spaces in the address are replaced with the `+` character. Multiple addresses are separated by a `|`.
- Destination addresses: Travel ending points. For example `&destinations=3734+Elvis+Presley+Blvd+Memphis+TN`
- The API key: Credentials for the request, in the form `&key=YOUR_API_KEY`.

Here's the entire request for the single origin and single destination shown
above after "Origin addresses" and "Destination addresses."  

```
https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=3610+Hacks+Cross+Rd+Memphis+TN&destinations=3734+Elvis+Presley+Blvd+Memphis+TN&key=YOUR_API_KEY
```

Here's the response to the request.  

```
{
   "destination_addresses" : [ "1921 Elvis Presley Blvd, Memphis, TN 38106, USA" ],
   "origin_addresses" : [ "3610 Hacks Cross Rd, Memphis, TN 38125, USA" ],
   "rows" : [
      {
         "elements" : [
            {
               "distance" : {
                  "text" : "15.2 mi",
                  "value" : 24392
               },
               "duration" : {
                  "text" : "21 mins",
                  "value" : 1264
               },
               "status" : "OK"
            }
         ]
      }
   ],
   "status" : "OK"
}
```

The response contains the travel distance (in miles and meters), and the travel
duration (in minutes and seconds), between the two addresses.

See the
[Distance Matrix API documentation](https://developers.google.com/maps/documentation/distance-matrix/start#sample-request)
for details about requests and responses.

### Compute the distance matrix

To compute the distance matrix, we would like to send a single request
containing all 16 addresses as both the origin and destination addresses.
However, we can't because this would require `16x16=256` origin-destination
pairs, while the API is restricted to 100 such pairs per request. So we need to
make multiple requests.

Since each row of the matrix contains 16 entries, we can compute at most six
rows per request (requiring `6x16=96` pairs). We can compute the whole matrix in
three requests, which return 6 rows, 6 rows, and 4 rows.

The following code computes the distance matrix as follows:

- Divide the 16 addresses into two groups of six addresses and one group of four addresses.
- For each group, build and send a request for the origin addresses in the group and all destination addresses. See [Build and send a request](https://developers.google.com/optimization/routing/vrp#send_request).
- Use the response to build the corresponding rows of the matrix, and concatenate the rows (which are just Python lists). See [Build rows of the distance matrix](https://developers.google.com/optimization/routing/vrp#create_the_data).

```python
def create_distance_matrix(data):
  addresses = data["addresses"]
  API_key = data["API_key"]
  # Distance Matrix API only accepts 100 elements per request, so get rows in multiple requests.
  max_elements = 100
  num_addresses = len(addresses) # 16 in this example.
  # Maximum number of rows that can be computed per request (6 in this example).
  max_rows = max_elements // num_addresses
  # num_addresses = q * max_rows + r (q = 2 and r = 4 in this example).
  q, r = divmod(num_addresses, max_rows)
  dest_addresses = addresses
  distance_matrix = []
  # Send q requests, returning max_rows rows per request.
  for i in range(q):
    origin_addresses = addresses[i * max_rows: (i + 1) * max_rows]
    response = send_request(origin_addresses, dest_addresses, API_key)
    distance_matrix += build_distance_matrix(response)

  # Get the remaining remaining r rows, if necessary.
  if r > 0:
    origin_addresses = addresses[q * max_rows: q * max_rows + r]
    response = send_request(origin_addresses, dest_addresses, API_key)
    distance_matrix += build_distance_matrix(response)
  return distance_matrix
```

### Build and send a request

The following function builds and sends a request for a given set of origin and
destination addresses.  

```python
def send_request(origin_addresses, dest_addresses, API_key):
  """ Build and send request for the given origin and destination addresses."""
  def build_address_str(addresses):
    # Build a pipe-separated string of addresses
    address_str = ''
    for i in range(len(addresses) - 1):
      address_str += addresses[i] + '|'
    address_str += addresses[-1]
    return address_str

  request = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial'
  origin_address_str = build_address_str(origin_addresses)
  dest_address_str = build_address_str(dest_addresses)
  request = request + '&origins=' + origin_address_str + '&destinations=' + \
                       dest_address_str + '&key=' + API_key
  jsonResult = urllib.urlopen(request).read()
  response = json.loads(jsonResult)
  return response
```

The sub-function `build_address_string` concatenates addresses separated by the
pipe character, `|`.

The remaining code in the function assembles the parts of the request described
above, and sends the request. The line  

```python
response = json.loads(jsonResult)
```

converts the raw result to a Python object.

### Build rows of the matrix

The following function builds rows of the distance matrix, using the response
returned by the `send_request` function.  

```python
def build_distance_matrix(response):
  distance_matrix = []
  for row in response['rows']:
    row_list = [row['elements'][j]['distance']['value'] for j in range(len(row['elements']))]
    distance_matrix.append(row_list)
  return distance_matrix
```

The line  

```python
row_list = [row['elements'][j]['distance']['value'] for j in range(len(row['elements']))]
```

extracts the distances between locations for a row of the response. You can
compare this with a portion of the response (converted by `json.loads`) for a
single origin and destination, shown below.  

```
{u'status': u'OK', u'rows':
[{u'elements': [{u'duration': {u'text': u'21 mins', u'value': 1264},
                 u'distance': {u'text': u'15.2 mi', u'value': 24392},
                 u'status': u'OK'}]}],
                 u'origin_addresses': [u'3610 Hacks Cross Rd, Memphis, TN 38125, USA'],
                 u'destination_addresses': [u'1921 Elvis Presley Blvd, Memphis, TN 38106, USA']}
```

If you want to create a time matrix, containing travel times between locations,
replace `'distance'` with `'duration'` in the function `build_distance_matrix`.

### Run the program

The following code in the main function runs the program  

```python
def main():
  """Entry point of the program"""
  # Create the data.
  data = create_data()
  addresses = data['addresses']
  API_key = data['API_key']
  distance_matrix = create_distance_matrix(data)
  print(distance_matrix)
```

When you run the program, it prints the distance matrix, as shown below.  

```
[[0, 24392, 33384, 14963, 31992, 32054, 20866, 28427, 15278, 21439, 28765, 34618, 35177, 10612, 26762, 27278],
 [25244, 0, 8314, 10784, 6922, 6984, 10678, 3270, 10707, 7873, 11350, 9548, 10107, 19176, 12139, 13609],
 [34062, 8491, 0, 14086, 4086, 1363, 11008, 4239, 13802, 9627, 7179, 1744, 925, 27994, 9730, 10531],
 [15494, 13289, 13938, 0, 11065, 12608, 4046, 10970, 581, 5226, 10788, 15500, 16059, 5797, 9180, 9450],
 [33351, 7780, 4096, 11348, 0, 2765, 7364, 4464, 11064, 6736, 3619, 4927, 5485, 20823, 6170, 7076],
 [32731, 7160, 1363, 12755, 2755, 0, 9677, 3703, 12471, 8297, 7265, 2279, 2096, 26664, 9816, 9554],
 [19636, 10678, 11017, 4038, 7398, 9687, 0, 9159, 3754, 2809, 7099, 10740, 11253, 8970, 5491, 5928],
 [29097, 3270, 4257, 11458, 4350, 3711, 9159, 0, 11174, 6354, 10160, 5178, 5258, 23029, 10620, 12419],
 [15809, 10707, 13654, 581, 10781, 12324, 3763, 10687, 0, 4943, 10504, 15216, 15775, 5216, 8896, 9166],
 [21831, 7873, 9406, 5226, 6282, 8075, 2809, 6354, 4943, 0, 6967, 10968, 11526, 10159, 5119, 6383],
 [28822, 11931, 6831, 11802, 3305, 6043, 7167, 10627, 11518, 7159, 0, 5361, 6422, 18351, 3267, 4068],
 [35116, 9545, 1771, 15206, 4648, 2518, 10967, 5382, 14922, 10747, 5909, 0, 1342, 29094, 8460, 9260],
 [36058, 10487, 927, 16148, 5590, 2211, 11420, 9183, 15864, 11689, 6734, 1392, 0, 30036, 9285, 10086],
 [11388, 19845, 28838, 5797, 20972, 27507, 8979, 23880, 5216, 10159, 18622, 29331, 29890, 0, 16618, 17135],
 [27151, 11444, 9719, 10131, 6193, 8945, 5913, 10421, 9847, 5374, 3335, 8249, 9309, 16680, 0, 1264],
 [27191, 14469, 10310, 9394, 7093, 9772, 5879, 13164, 9110, 6422, 3933, 8840, 9901, 16720, 1288, 0]]
```

### Travel time matrix

As mentioned [above](https://developers.google.com/optimization/routing/vrp#build_and_send_a_request), it you want to create a matrix of travel
times between locations (instead of distances), simply replace `'distance'` with
`'duration'` in the function `build_distance_matrix`. When you run the program
with that change, it displays the following travel time matrix:  

```
[[0, 1232, 1599, 964, 1488, 1441, 1291, 1323, 978, 1228, 1493, 1617, 1570, 765, 1272, 1359],
[1333, 0, 653, 922, 542, 495, 864, 297, 917, 622, 783, 671, 624, 1059, 985, 904],
[1669, 643, 0, 1291, 447, 161, 1021, 461, 1258, 862, 715, 419, 198, 1395, 855, 904],
[1062, 862, 1262, 0, 946, 1104, 360, 926, 61, 482, 995, 1237, 1190, 589, 761, 839],
[1626, 600, 475, 1008, 0, 317, 688, 505, 976, 630, 446, 475, 428, 1271, 587, 648],
[1537, 511, 166, 1158, 314, 0, 889, 402, 1125, 730, 697, 430, 313, 1262, 837, 770],
[1388, 891, 1022, 374, 668, 863, 0, 731, 341, 259, 731, 1110, 1091, 869, 496, 570],
[1407, 303, 489, 934, 492, 410, 725, 0, 901, 482, 692, 580, 587, 1132, 845, 814],
[1060, 914, 1215, 55, 899, 1057, 314, 880, 0, 435, 949, 1190, 1144, 528, 714, 792],
[1314, 651, 855, 475, 605, 696, 260, 491, 443, 0, 700, 830, 783, 970, 489, 596],
[1530, 801, 697, 990, 427, 625, 709, 721, 957, 663, 0, 542, 634, 1084, 338, 387],
[1704, 678, 370, 1355, 508, 430, 1074, 598, 1322, 866, 564, 0, 297, 1405, 703, 752],
[1612, 586, 215, 1201, 416, 359, 1070, 506, 1169, 773, 639, 313, 0, 1312, 778, 827],
[861, 1074, 1441, 610, 1337, 1282, 869, 1164, 555, 990, 1157, 1433, 1386, 0, 936, 1022],
[1375, 1045, 899, 795, 629, 825, 588, 901, 762, 549, 408, 744, 836, 929, 0, 107],
[1428, 947, 957, 885, 692, 750, 599, 867, 852, 637, 362, 803, 894, 982, 111, 0]]
```

### Using the distance matrix in a VRP program

To see how to use the distance matrix shown above in a VRP program, replace the
distance matrix in the previous [VRP example](https://developers.google.com/optimization/routing/vrp#complete_programs) with the one
above. Also, change the value of the `maximum_distance` parameter in the
distance dimension to `70000`. When you run the modified program, it returns the
following output.  

```
Route for vehicle 0:
 0 -> 1 -> 7 -> 5 -> 4 -> 8 -> 0
Distance of route: 61001m

Route for vehicle 1:
 0 -> 0
Distance of route: 0m

Route for vehicle 2:
 0 -> 3 -> 2 -> 12 -> 11 -> 6 -> 0
Distance of route: 61821m

Route for vehicle 3:
 0 -> 13 -> 9 -> 10 -> 14 -> 15 -> 0
Distance of route: 59460m

Total distance of all routes: 182282m
```

### Entire program

The entire program is shown below.  

```python
import requests
import json
import urllib


def create_data():
  """Creates the data."""
  data = {}
  data['API_key'] = 'YOUR_API_KEY'
  data['addresses'] = ['3610+Hacks+Cross+Rd+Memphis+TN', # depot
                       '1921+Elvis+Presley+Blvd+Memphis+TN',
                       '149+Union+Avenue+Memphis+TN',
                       '1034+Audubon+Drive+Memphis+TN',
                       '1532+Madison+Ave+Memphis+TN',
                       '706+Union+Ave+Memphis+TN',
                       '3641+Central+Ave+Memphis+TN',
                       '926+E+McLemore+Ave+Memphis+TN',
                       '4339+Park+Ave+Memphis+TN',
                       '600+Goodwyn+St+Memphis+TN',
                       '2000+North+Pkwy+Memphis+TN',
                       '262+Danny+Thomas+Pl+Memphis+TN',
                       '125+N+Front+St+Memphis+TN',
                       '5959+Park+Ave+Memphis+TN',
                       '814+Scott+St+Memphis+TN',
                       '1005+Tillman+St+Memphis+TN'
                      ]
  return data

def create_distance_matrix(data):
  addresses = data["addresses"]
  API_key = data["API_key"]
  # Distance Matrix API only accepts 100 elements per request, so get rows in multiple requests.
  max_elements = 100
  num_addresses = len(addresses) # 16 in this example.
  # Maximum number of rows that can be computed per request (6 in this example).
  max_rows = max_elements // num_addresses
  # num_addresses = q * max_rows + r (q = 2 and r = 4 in this example).
  q, r = divmod(num_addresses, max_rows)
  dest_addresses = addresses
  distance_matrix = []
  # Send q requests, returning max_rows rows per request.
  for i in range(q):
    origin_addresses = addresses[i * max_rows: (i + 1) * max_rows]
    response = send_request(origin_addresses, dest_addresses, API_key)
    distance_matrix += build_distance_matrix(response)

  # Get the remaining remaining r rows, if necessary.
  if r > 0:
    origin_addresses = addresses[q * max_rows: q * max_rows + r]
    response = send_request(origin_addresses, dest_addresses, API_key)
    distance_matrix += build_distance_matrix(response)
  return distance_matrix

def send_request(origin_addresses, dest_addresses, API_key):
  """ Build and send request for the given origin and destination addresses."""
  def build_address_str(addresses):
    # Build a pipe-separated string of addresses
    address_str = ''
    for i in range(len(addresses) - 1):
      address_str += addresses[i] + '|'
    address_str += addresses[-1]
    return address_str

  request = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial'
  origin_address_str = build_address_str(origin_addresses)
  dest_address_str = build_address_str(dest_addresses)
  request = request + '&origins=' + origin_address_str + '&destinations=' + \
                       dest_address_str + '&key=' + API_key
  jsonResult = urllib.urlopen(request).read()
  response = json.loads(jsonResult)
  return response

def build_distance_matrix(response):
  distance_matrix = []
  for row in response['rows']:
    row_list = [row['elements'][j]['distance']['value'] for j in range(len(row['elements']))]
    distance_matrix.append(row_list)
  return distance_matrix

########
# Main #
########
def main():
  """Entry point of the program"""
  # Create the data.
  data = create_data()
  addresses = data['addresses']
  API_key = data['API_key']
  distance_matrix = create_distance_matrix(data)
  print(distance_matrix)
if __name__ == '__main__':
  main()
```


# Vehicle Routing Problem with Time Windows

Many vehicle routing problems involve scheduling visits to customers who are
only available during specific time windows.

These problems are known as *vehicle routing problems with time windows* (VRPTWs).

## VRPTW Example

On this page, we'll walk through an example that shows how to solve a VRPTW.
Since the problem involves time windows, the data include a **time matrix**,
which contains the travel times between locations (rather than a distance matrix
as in previous examples).

The diagram below shows the locations to visit in blue and the depot in black.
The time windows are shown above each location. See
[Location coordinates](https://developers.google.com/optimization/routing/vrp#location_coordinates) in the
VRP section for more details about how the locations are defined.

The goal is to minimize the total travel time of the vehicles.

![](https://developers.google.com/static/optimization/images/routing/vrptw.svg)

## Solving the VRPTW example with OR-Tools

The following sections describe how to solve the VRPTW example with OR-Tools.

### Create the data

The following function creates the data for the problem.  

### Python

```python
def create_data_model():
    """Stores the data for the problem."""
    data = {}
    data["time_matrix"] = [
        [0, 6, 9, 8, 7, 3, 6, 2, 3, 2, 6, 6, 4, 4, 5, 9, 7],
        [6, 0, 8, 3, 2, 6, 8, 4, 8, 8, 13, 7, 5, 8, 12, 10, 14],
        [9, 8, 0, 11, 10, 6, 3, 9, 5, 8, 4, 15, 14, 13, 9, 18, 9],
        [8, 3, 11, 0, 1, 7, 10, 6, 10, 10, 14, 6, 7, 9, 14, 6, 16],
        [7, 2, 10, 1, 0, 6, 9, 4, 8, 9, 13, 4, 6, 8, 12, 8, 14],
        [3, 6, 6, 7, 6, 0, 2, 3, 2, 2, 7, 9, 7, 7, 6, 12, 8],
        [6, 8, 3, 10, 9, 2, 0, 6, 2, 5, 4, 12, 10, 10, 6, 15, 5],
        [2, 4, 9, 6, 4, 3, 6, 0, 4, 4, 8, 5, 4, 3, 7, 8, 10],
        [3, 8, 5, 10, 8, 2, 2, 4, 0, 3, 4, 9, 8, 7, 3, 13, 6],
        [2, 8, 8, 10, 9, 2, 5, 4, 3, 0, 4, 6, 5, 4, 3, 9, 5],
        [6, 13, 4, 14, 13, 7, 4, 8, 4, 4, 0, 10, 9, 8, 4, 13, 4],
        [6, 7, 15, 6, 4, 9, 12, 5, 9, 6, 10, 0, 1, 3, 7, 3, 10],
        [4, 5, 14, 7, 6, 7, 10, 4, 8, 5, 9, 1, 0, 2, 6, 4, 8],
        [4, 8, 13, 9, 8, 7, 10, 3, 7, 4, 8, 3, 2, 0, 4, 5, 6],
        [5, 12, 9, 14, 12, 6, 6, 7, 3, 3, 4, 7, 6, 4, 0, 9, 2],
        [9, 10, 18, 6, 8, 12, 15, 8, 13, 9, 13, 3, 4, 5, 9, 0, 9],
        [7, 14, 9, 16, 14, 8, 5, 10, 6, 5, 4, 10, 8, 6, 2, 9, 0],
    ]
    data["time_windows"] = [
        (0, 5),  # depot
        (7, 12),  # 1
        (10, 15),  # 2
        (16, 18),  # 3
        (10, 13),  # 4
        (0, 5),  # 5
        (5, 10),  # 6
        (0, 4),  # 7
        (5, 10),  # 8
        (0, 3),  # 9
        (10, 16),  # 10
        (10, 15),  # 11
        (0, 5),  # 12
        (5, 10),  # 13
        (7, 8),  # 14
        (10, 15),  # 15
        (11, 15),  # 16
    ]
    data["num_vehicles"] = 4
    data["depot"] = 0
    return data
```
The data consists of:

- `data['time_matrix']`: An array of travel times between locations. Note that this differs from previous examples, which use a distance matrix. If all vehicles travel at the same speed, you will get the same solution if you use a distance matrix or a time matrix, since travel distances are a constant multiple of travel times.
- `data['time_windows']`: An array of time windows for the locations, which you can think of as requested times for a visit. Vehicles must visit a location within its time window.
- `data['num_vehicles']`: The number of vehicles in the fleet.
- `data['depot']`: The index of the depot.

### C++

```c++
struct DataModel {
  const std::vector<std::vector<int64_t>> time_matrix{
      {0, 6, 9, 8, 7, 3, 6, 2, 3, 2, 6, 6, 4, 4, 5, 9, 7},
      {6, 0, 8, 3, 2, 6, 8, 4, 8, 8, 13, 7, 5, 8, 12, 10, 14},
      {9, 8, 0, 11, 10, 6, 3, 9, 5, 8, 4, 15, 14, 13, 9, 18, 9},
      {8, 3, 11, 0, 1, 7, 10, 6, 10, 10, 14, 6, 7, 9, 14, 6, 16},
      {7, 2, 10, 1, 0, 6, 9, 4, 8, 9, 13, 4, 6, 8, 12, 8, 14},
      {3, 6, 6, 7, 6, 0, 2, 3, 2, 2, 7, 9, 7, 7, 6, 12, 8},
      {6, 8, 3, 10, 9, 2, 0, 6, 2, 5, 4, 12, 10, 10, 6, 15, 5},
      {2, 4, 9, 6, 4, 3, 6, 0, 4, 4, 8, 5, 4, 3, 7, 8, 10},
      {3, 8, 5, 10, 8, 2, 2, 4, 0, 3, 4, 9, 8, 7, 3, 13, 6},
      {2, 8, 8, 10, 9, 2, 5, 4, 3, 0, 4, 6, 5, 4, 3, 9, 5},
      {6, 13, 4, 14, 13, 7, 4, 8, 4, 4, 0, 10, 9, 8, 4, 13, 4},
      {6, 7, 15, 6, 4, 9, 12, 5, 9, 6, 10, 0, 1, 3, 7, 3, 10},
      {4, 5, 14, 7, 6, 7, 10, 4, 8, 5, 9, 1, 0, 2, 6, 4, 8},
      {4, 8, 13, 9, 8, 7, 10, 3, 7, 4, 8, 3, 2, 0, 4, 5, 6},
      {5, 12, 9, 14, 12, 6, 6, 7, 3, 3, 4, 7, 6, 4, 0, 9, 2},
      {9, 10, 18, 6, 8, 12, 15, 8, 13, 9, 13, 3, 4, 5, 9, 0, 9},
      {7, 14, 9, 16, 14, 8, 5, 10, 6, 5, 4, 10, 8, 6, 2, 9, 0},
  };
  const std::vector<std::pair<int64_t, int64_t>> time_windows{
      {0, 5},    // depot
      {7, 12},   // 1
      {10, 15},  // 2
      {16, 18},  // 3
      {10, 13},  // 4
      {0, 5},    // 5
      {5, 10},   // 6
      {0, 4},    // 7
      {5, 10},   // 8
      {0, 3},    // 9
      {10, 16},  // 10
      {10, 15},  // 11
      {0, 5},    // 12
      {5, 10},   // 13
      {7, 8},    // 14
      {10, 15},  // 15
      {11, 15},  // 16
  };
  const int num_vehicles = 4;
  const RoutingIndexManager::NodeIndex depot{0};
};
```
The data consists of:

- `time_matrix`: An array of travel times between locations. Note that this differs from previous examples, which use a distance matrix. If all vehicles travel at the same speed, you will get the same solution if you use a distance matrix or a time matrix, since travel distances are a constant multiple of travel times.
- `time_windows`: An array of time windows for the locations, which you can think of as requested times for a visit. Vehicles must visit a location within its time window.
- `num_vehicles`: The number of vehicles in the fleet.
- `depot`: The index of the depot.

### Java

```java
static class DataModel {
  public final long[][] timeMatrix = {
      {0, 6, 9, 8, 7, 3, 6, 2, 3, 2, 6, 6, 4, 4, 5, 9, 7},
      {6, 0, 8, 3, 2, 6, 8, 4, 8, 8, 13, 7, 5, 8, 12, 10, 14},
      {9, 8, 0, 11, 10, 6, 3, 9, 5, 8, 4, 15, 14, 13, 9, 18, 9},
      {8, 3, 11, 0, 1, 7, 10, 6, 10, 10, 14, 6, 7, 9, 14, 6, 16},
      {7, 2, 10, 1, 0, 6, 9, 4, 8, 9, 13, 4, 6, 8, 12, 8, 14},
      {3, 6, 6, 7, 6, 0, 2, 3, 2, 2, 7, 9, 7, 7, 6, 12, 8},
      {6, 8, 3, 10, 9, 2, 0, 6, 2, 5, 4, 12, 10, 10, 6, 15, 5},
      {2, 4, 9, 6, 4, 3, 6, 0, 4, 4, 8, 5, 4, 3, 7, 8, 10},
      {3, 8, 5, 10, 8, 2, 2, 4, 0, 3, 4, 9, 8, 7, 3, 13, 6},
      {2, 8, 8, 10, 9, 2, 5, 4, 3, 0, 4, 6, 5, 4, 3, 9, 5},
      {6, 13, 4, 14, 13, 7, 4, 8, 4, 4, 0, 10, 9, 8, 4, 13, 4},
      {6, 7, 15, 6, 4, 9, 12, 5, 9, 6, 10, 0, 1, 3, 7, 3, 10},
      {4, 5, 14, 7, 6, 7, 10, 4, 8, 5, 9, 1, 0, 2, 6, 4, 8},
      {4, 8, 13, 9, 8, 7, 10, 3, 7, 4, 8, 3, 2, 0, 4, 5, 6},
      {5, 12, 9, 14, 12, 6, 6, 7, 3, 3, 4, 7, 6, 4, 0, 9, 2},
      {9, 10, 18, 6, 8, 12, 15, 8, 13, 9, 13, 3, 4, 5, 9, 0, 9},
      {7, 14, 9, 16, 14, 8, 5, 10, 6, 5, 4, 10, 8, 6, 2, 9, 0},
  };
  public final long[][] timeWindows = {
      {0, 5}, // depot
      {7, 12}, // 1
      {10, 15}, // 2
      {16, 18}, // 3
      {10, 13}, // 4
      {0, 5}, // 5
      {5, 10}, // 6
      {0, 4}, // 7
      {5, 10}, // 8
      {0, 3}, // 9
      {10, 16}, // 10
      {10, 15}, // 11
      {0, 5}, // 12
      {5, 10}, // 13
      {7, 8}, // 14
      {10, 15}, // 15
      {11, 15}, // 16
  };
  public final int vehicleNumber = 4;
  public final int depot = 0;
}
```
The data consists of:

- `timeMatrix`: An array of travel times between locations. Note that this differs from previous examples, which use a distance matrix. If all vehicles travel at the same speed, you will get the same solution if you use a distance matrix or a time matrix, since travel distances are a constant multiple of travel times.
- `timeWindows`: An array of time windows for the locations, which you can think of as requested times for a visit. Vehicles must visit a location within its time window.
- `vehicleNumber`: The number of vehicles in the fleet.
- `depot`: The index of the depot.

### C#

```c#
class DataModel
{
    public long[,] TimeMatrix = {
        { 0, 6, 9, 8, 7, 3, 6, 2, 3, 2, 6, 6, 4, 4, 5, 9, 7 },
        { 6, 0, 8, 3, 2, 6, 8, 4, 8, 8, 13, 7, 5, 8, 12, 10, 14 },
        { 9, 8, 0, 11, 10, 6, 3, 9, 5, 8, 4, 15, 14, 13, 9, 18, 9 },
        { 8, 3, 11, 0, 1, 7, 10, 6, 10, 10, 14, 6, 7, 9, 14, 6, 16 },
        { 7, 2, 10, 1, 0, 6, 9, 4, 8, 9, 13, 4, 6, 8, 12, 8, 14 },
        { 3, 6, 6, 7, 6, 0, 2, 3, 2, 2, 7, 9, 7, 7, 6, 12, 8 },
        { 6, 8, 3, 10, 9, 2, 0, 6, 2, 5, 4, 12, 10, 10, 6, 15, 5 },
        { 2, 4, 9, 6, 4, 3, 6, 0, 4, 4, 8, 5, 4, 3, 7, 8, 10 },
        { 3, 8, 5, 10, 8, 2, 2, 4, 0, 3, 4, 9, 8, 7, 3, 13, 6 },
        { 2, 8, 8, 10, 9, 2, 5, 4, 3, 0, 4, 6, 5, 4, 3, 9, 5 },
        { 6, 13, 4, 14, 13, 7, 4, 8, 4, 4, 0, 10, 9, 8, 4, 13, 4 },
        { 6, 7, 15, 6, 4, 9, 12, 5, 9, 6, 10, 0, 1, 3, 7, 3, 10 },
        { 4, 5, 14, 7, 6, 7, 10, 4, 8, 5, 9, 1, 0, 2, 6, 4, 8 },
        { 4, 8, 13, 9, 8, 7, 10, 3, 7, 4, 8, 3, 2, 0, 4, 5, 6 },
        { 5, 12, 9, 14, 12, 6, 6, 7, 3, 3, 4, 7, 6, 4, 0, 9, 2 },
        { 9, 10, 18, 6, 8, 12, 15, 8, 13, 9, 13, 3, 4, 5, 9, 0, 9 },
        { 7, 14, 9, 16, 14, 8, 5, 10, 6, 5, 4, 10, 8, 6, 2, 9, 0 },
    };
    public long[,] TimeWindows = {
        { 0, 5 },   // depot
        { 7, 12 },  // 1
        { 10, 15 }, // 2
        { 16, 18 }, // 3
        { 10, 13 }, // 4
        { 0, 5 },   // 5
        { 5, 10 },  // 6
        { 0, 4 },   // 7
        { 5, 10 },  // 8
        { 0, 3 },   // 9
        { 10, 16 }, // 10
        { 10, 15 }, // 11
        { 0, 5 },   // 12
        { 5, 10 },  // 13
        { 7, 8 },   // 14
        { 10, 15 }, // 15
        { 11, 15 }, // 16
    };
    public int VehicleNumber = 4;
    public int Depot = 0;
};
```
The data consists of:

- `TimeMatrix`: An array of travel times between locations. Note that this differs from previous examples, which use a distance matrix. If all vehicles travel at the same speed, you will get the same solution if you use a distance matrix or a time matrix, since travel distances are a constant multiple of travel times.
- `TimeWindows`: An array of time windows for the locations, which you can think of as requested times for a visit. Vehicles must visit a location within its time window.
- `VehicleNumber`: The number of vehicles in the fleet.
- `Depot`: The index of the depot.

### Time callback

The following function creates the time callback and passes it to the solver. It
also sets the arc costs, which define the cost of travel, to be the travel times
between locations.  

### Python

```python
def time_callback(from_index, to_index):
    """Returns the travel time between the two nodes."""
    # Convert from routing variable Index to time matrix NodeIndex.
    from_node = manager.IndexToNode(from_index)
    to_node = manager.IndexToNode(to_index)
    return data["time_matrix"][from_node][to_node]

transit_callback_index = routing.RegisterTransitCallback(time_callback)
routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
```

### C++

```c++
const int transit_callback_index = routing.RegisterTransitCallback(
    [&data, &manager](const int64_t from_index,
                      const int64_t to_index) -> int64_t {
      // Convert from routing variable Index to time matrix NodeIndex.
      const int from_node = manager.IndexToNode(from_index).value();
      const int to_node = manager.IndexToNode(to_index).value();
      return data.time_matrix[from_node][to_node];
    });
routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index);
```

### Java

```java
final int transitCallbackIndex =
    routing.registerTransitCallback((long fromIndex, long toIndex) -> {
      // Convert from routing variable Index to user NodeIndex.
      int fromNode = manager.indexToNode(fromIndex);
      int toNode = manager.indexToNode(toIndex);
      return data.timeMatrix[fromNode][toNode];
    });
routing.setArcCostEvaluatorOfAllVehicles(transitCallbackIndex);
```

### C#

```c#
int transitCallbackIndex = routing.RegisterTransitCallback((long fromIndex, long toIndex) =>
                                                           {
                                                               // Convert from routing variable Index to time
                                                               // matrix NodeIndex.
                                                               var fromNode = manager.IndexToNode(fromIndex);
                                                               var toNode = manager.IndexToNode(toIndex);
                                                               return data.TimeMatrix[fromNode, toNode];
                                                           });
routing.SetArcCostEvaluatorOfAllVehicles(transitCallbackIndex);
```

### Add time window constraints

The following code adds time window constraints for all locations.  

### Python

```python
time = "Time"
routing.AddDimension(
    transit_callback_index,
    30,  # allow waiting time
    30,  # maximum time per vehicle
    False,  # Don't force start cumul to zero.
    time,
)
time_dimension = routing.GetDimensionOrDie(time)
# Add time window constraints for each location except depot.
for location_idx, time_window in enumerate(data["time_windows"]):
    if location_idx == data["depot"]:
        continue
    index = manager.NodeToIndex(location_idx)
    time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])
# Add time window constraints for each vehicle start node.
depot_idx = data["depot"]
for vehicle_id in range(data["num_vehicles"]):
    index = routing.Start(vehicle_id)
    time_dimension.CumulVar(index).SetRange(
        data["time_windows"][depot_idx][0], data["time_windows"][depot_idx][1]
    )
for i in range(data["num_vehicles"]):
    routing.AddVariableMinimizedByFinalizer(
        time_dimension.CumulVar(routing.Start(i))
    )
    routing.AddVariableMinimizedByFinalizer(time_dimension.CumulVar(routing.End(i)))
```

### C++

```c++
const std::string time = "Time";
routing.AddDimension(transit_callback_index,  // transit callback index
                     int64_t{30},             // allow waiting time
                     int64_t{30},             // maximum time per vehicle
                     false,  // Don't force start cumul to zero
                     time);
const RoutingDimension& time_dimension = routing.GetDimensionOrDie(time);
// Add time window constraints for each location except depot.
for (int i = 1; i < data.time_windows.size(); ++i) {
  const int64_t index =
      manager.NodeToIndex(RoutingIndexManager::NodeIndex(i));
  time_dimension.CumulVar(index)->SetRange(data.time_windows[i].first,
                                           data.time_windows[i].second);
}
// Add time window constraints for each vehicle start node.
for (int i = 0; i < data.num_vehicles; ++i) {
  const int64_t index = routing.Start(i);
  time_dimension.CumulVar(index)->SetRange(data.time_windows[0].first,
                                           data.time_windows[0].second);
}
for (int i = 0; i < data.num_vehicles; ++i) {
  routing.AddVariableMinimizedByFinalizer(
      time_dimension.CumulVar(routing.Start(i)));
  routing.AddVariableMinimizedByFinalizer(
      time_dimension.CumulVar(routing.End(i)));
}
```

### Java

```java
boolean unused = routing.addDimension(transitCallbackIndex, // transit callback
    30, // allow waiting time
    30, // vehicle maximum capacities
    false, // start cumul to zero
    "Time");
RoutingDimension timeDimension = routing.getMutableDimension("Time");
// Add time window constraints for each location except depot.
for (int i = 1; i < data.timeWindows.length; ++i) {
  long index = manager.nodeToIndex(i);
  timeDimension.cumulVar(index).setRange(data.timeWindows[i][0], data.timeWindows[i][1]);
}
// Add time window constraints for each vehicle start node.
for (int i = 0; i < data.vehicleNumber; ++i) {
  long index = routing.start(i);
  timeDimension.cumulVar(index).setRange(data.timeWindows[0][0], data.timeWindows[0][1]);
}
for (int i = 0; i < data.vehicleNumber; ++i) {
  routing.addVariableMinimizedByFinalizer(timeDimension.cumulVar(routing.start(i)));
  routing.addVariableMinimizedByFinalizer(timeDimension.cumulVar(routing.end(i)));
}
```

### C#

```c#
routing.AddDimension(transitCallbackIndex, // transit callback
                     30,                   // allow waiting time
                     30,                   // vehicle maximum capacities
                     false,                // start cumul to zero
                     "Time");
RoutingDimension timeDimension = routing.GetMutableDimension("Time");
// Add time window constraints for each location except depot.
for (int i = 1; i < data.TimeWindows.GetLength(0); ++i)
{
    long index = manager.NodeToIndex(i);
    timeDimension.CumulVar(index).SetRange(data.TimeWindows[i, 0], data.TimeWindows[i, 1]);
}
// Add time window constraints for each vehicle start node.
for (int i = 0; i < data.VehicleNumber; ++i)
{
    long index = routing.Start(i);
    timeDimension.CumulVar(index).SetRange(data.TimeWindows[0, 0], data.TimeWindows[0, 1]);
}
for (int i = 0; i < data.VehicleNumber; ++i)
{
    routing.AddVariableMinimizedByFinalizer(timeDimension.CumulVar(routing.Start(i)));
    routing.AddVariableMinimizedByFinalizer(timeDimension.CumulVar(routing.End(i)));
}
```

The code creates a [dimension](https://developers.google.com/optimization/routing/dimensions) for the travel
time of the vehicles, similar to the dimensions for travel distance or demands
in previous examples. Dimensions keep track of quantities that accumulate over a
vehicle's route. In the code above, `time_dimension.CumulVar(index)` is
the cumulative travel time when a vehicle arrives at the
location with the given `index`.

The dimension is created using the `AddDimension` method, which has the
following arguments:

- The index for the travel time callback: `transit_callback_index`
- An upper bound for slack (the wait times at the locations): `30`. While this was set to 0 in the [CVRP example](https://developers.google.com/optimization/routing/cvrp#demand), the VRPTW has to allow positive wait time due to the time window constraints.
- An upper bound for the total time over each vehicle's route: `30`
- A boolean variable that specifies whether the cumulative variable is set to zero at the start of each vehicle's route.
- The name of the dimension.

Next, the lines  

### Python

```python
for location_idx, time_window in enumerate(data["time_windows"]):
    if location_idx == data["depot"]:
        continue
    index = manager.NodeToIndex(location_idx)
    time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])
```

### C++

```c++
for (int i = 1; i < data.time_windows.size(); ++i) {
  const int64_t index =
      manager.NodeToIndex(RoutingIndexManager::NodeIndex(i));
  time_dimension.CumulVar(index)->SetRange(data.time_windows[i].first,
                                           data.time_windows[i].second);
}
```

### Java

```java
for (int i = 1; i < data.timeWindows.length; ++i) {
  long index = manager.nodeToIndex(i);
  timeDimension.cumulVar(index).setRange(data.timeWindows[i][0], data.timeWindows[i][1]);
}
```

### C#

```c#
for (int i = 1; i < data.TimeWindows.GetLength(0); ++i)
{
    long index = manager.NodeToIndex(i);
    timeDimension.CumulVar(index).SetRange(data.TimeWindows[i, 0], data.TimeWindows[i, 1]);
}
```

require that a vehicle must visit a location during the location's time window.

### Set search parameters

The following code sets the default search parameters and a heuristic method for
finding the first solution:  

### Python

```python
search_parameters = pywrapcp.DefaultRoutingSearchParameters()
search_parameters.first_solution_strategy = (
    routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
)
```

### C++

```c++
RoutingSearchParameters searchParameters = DefaultRoutingSearchParameters();
searchParameters.set_first_solution_strategy(
    FirstSolutionStrategy::PATH_CHEAPEST_ARC);
```

### Java

```java
RoutingSearchParameters searchParameters =
    main.defaultRoutingSearchParameters()
        .toBuilder()
        .setFirstSolutionStrategy(FirstSolutionStrategy.Value.PATH_CHEAPEST_ARC)
        .build();
```

### C#

```c#
RoutingSearchParameters searchParameters =
    operations_research_constraint_solver.DefaultRoutingSearchParameters();
searchParameters.FirstSolutionStrategy = FirstSolutionStrategy.Types.Value.PathCheapestArc;
```

### Add the solution printer

The function that displays the solution is shown below.  

### Python

```python
def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f"Objective: {solution.ObjectiveValue()}")
    time_dimension = routing.GetDimensionOrDie("Time")
    total_time = 0
    for vehicle_id in range(data["num_vehicles"]):
        if not routing.IsVehicleUsed(solution, vehicle_id):
            continue
        index = routing.Start(vehicle_id)
        plan_output = f"Route for vehicle {vehicle_id}:\n"
        while not routing.IsEnd(index):
            time_var = time_dimension.CumulVar(index)
            plan_output += (
                f"{manager.IndexToNode(index)}"
                f" Time({solution.Min(time_var)},{solution.Max(time_var)})"
                " -> "
            )
            index = solution.Value(routing.NextVar(index))
        time_var = time_dimension.CumulVar(index)
        plan_output += (
            f"{manager.IndexToNode(index)}"
            f" Time({solution.Min(time_var)},{solution.Max(time_var)})\n"
        )
        plan_output += f"Time of the route: {solution.Min(time_var)}min\n"
        print(plan_output)
        total_time += solution.Min(time_var)
    print(f"Total time of all routes: {total_time}min")
```

### C++

```c++
//! @brief Print the solution.
//! @param[in] data Data of the problem.
//! @param[in] manager Index manager used.
//! @param[in] routing Routing solver used.
//! @param[in] solution Solution found by the solver.
void PrintSolution(const DataModel& data, const RoutingIndexManager& manager,
                   const RoutingModel& routing, const Assignment& solution) {
  const RoutingDimension& time_dimension = routing.GetDimensionOrDie("Time");
  int64_t total_time{0};
  for (int vehicle_id = 0; vehicle_id < data.num_vehicles; ++vehicle_id) {
    if (!routing.IsVehicleUsed(solution, vehicle_id)) {
      continue;
    }
    int64_t index = routing.Start(vehicle_id);
    LOG(INFO) << "Route for vehicle " << vehicle_id << ":";
    std::ostringstream route;
    while (!routing.IsEnd(index)) {
      auto time_var = time_dimension.CumulVar(index);
      route << manager.IndexToNode(index).value() << " Time("
            << solution.Min(time_var) << ", " << solution.Max(time_var)
            << ") -> ";
      index = solution.Value(routing.NextVar(index));
    }
    auto time_var = time_dimension.CumulVar(index);
    LOG(INFO) << route.str() << manager.IndexToNode(index).value() << " Time("
              << solution.Min(time_var) << ", " << solution.Max(time_var)
              << ")";
    LOG(INFO) << "Time of the route: " << solution.Min(time_var) << "min";
    total_time += solution.Min(time_var);
  }
  LOG(INFO) << "Total time of all routes: " << total_time << "min";
  LOG(INFO) << "";
  LOG(INFO) << "Advanced usage:";
  LOG(INFO) << "Problem solved in " << routing.solver()->wall_time() << "ms";
}
```

### Java

```java
/// @brief Print the solution.
static void printSolution(
    DataModel data, RoutingModel routing, RoutingIndexManager manager, Assignment solution) {
  // Solution cost.
  logger.info("Objective : " + solution.objectiveValue());
  // Inspect solution.
  RoutingDimension timeDimension = routing.getMutableDimension("Time");
  long totalTime = 0;
  for (int i = 0; i < data.vehicleNumber; ++i) {
    if (!routing.isVehicleUsed(solution, i)) {
      continue;
    }
    long index = routing.start(i);
    logger.info("Route for Vehicle " + i + ":");
    String route = "";
    while (!routing.isEnd(index)) {
      IntVar timeVar = timeDimension.cumulVar(index);
      route += manager.indexToNode(index) + " Time(" + solution.min(timeVar) + ","
          + solution.max(timeVar) + ") -> ";
      index = solution.value(routing.nextVar(index));
    }
    IntVar timeVar = timeDimension.cumulVar(index);
    route += manager.indexToNode(index) + " Time(" + solution.min(timeVar) + ","
        + solution.max(timeVar) + ")";
    logger.info(route);
    logger.info("Time of the route: " + solution.min(timeVar) + "min");
    totalTime += solution.min(timeVar);
  }
  logger.info("Total time of all routes: " + totalTime + "min");
}
```

### C#

```c#
/// <summary>
///   Print the solution.
/// </summary>
static void PrintSolution(in DataModel data, in RoutingModel routing, in RoutingIndexManager manager,
                          in Assignment solution)
{
    Console.WriteLine($"Objective {solution.ObjectiveValue()}:");

    // Inspect solution.
    RoutingDimension timeDimension = routing.GetMutableDimension("Time");
    long totalTime = 0;
    for (int i = 0; i < data.VehicleNumber; ++i)
    {
        if (!routing.IsVehicleUsed(solution, i))
        {
            continue;
        }
        Console.WriteLine("Route for Vehicle {0}:", i);
        var index = routing.Start(i);
        while (routing.IsEnd(index) == false)
        {
            var timeVar = timeDimension.CumulVar(index);
            Console.Write("{0} Time({1},{2}) -> ", manager.IndexToNode(index), solution.Min(timeVar),
                          solution.Max(timeVar));
            index = solution.Value(routing.NextVar(index));
        }
        var endTimeVar = timeDimension.CumulVar(index);
        Console.WriteLine("{0} Time({1},{2})", manager.IndexToNode(index), solution.Min(endTimeVar),
                          solution.Max(endTimeVar));
        Console.WriteLine("Time of the route: {0}min", solution.Min(endTimeVar));
        totalTime += solution.Min(endTimeVar);
    }
    Console.WriteLine("Total time of all routes: {0}min", totalTime);
}
```

The solution displays the vehicle routes, and the **solution window** at each
location, as explained in the next section.

### Solution windows

The **solution window** at a location is the time interval during which a
vehicle must arrive, in order to stay on schedule.The solution window is
contained in---and usually smaller than---the
[constraint time window](https://developers.google.com/optimization/routing/vrptw#time_window_constraints) at the location.

In the solution printer function above, the solution window is returned by
`(assignment.Min(time_var), assignment.Max(time_var)` where
`time_var = time_dimension.CumulVar(index)` is the vehicle's cumulative travel
time at the location.

If the minimum and maximum values of `time_var` are the same, the solution
window is a single point in time, which means the vehicle must depart from the
location as soon as it arrives. On the other hand, if the minimum is less than
the maximum, the vehicle can wait before departing.

The section [Running the program](https://developers.google.com/optimization/routing/vrptw#solution) describes the solution windows for
this example.

### Solve

The main function for this example is similar to the one for the
[TSP example](https://developers.google.com/optimization/routing/tsp#create_model).  

### Python

```python
solution = routing.SolveWithParameters(search_parameters)
```

### C++

```c++
const Assignment* solution = routing.SolveWithParameters(searchParameters);
```

### Java

```java
Assignment solution = routing.solveWithParameters(searchParameters);
```

### C#

```c#
Assignment solution = routing.SolveWithParameters(searchParameters);
```

### Running the program

When you run the [program](https://developers.google.com/optimization/routing/vrptw#program), it displays the
following output:  

```
Route for vehicle 0:
 0 Time(0,0) ->  9 Time(2,3) ->  14 Time(7,8) -> 16 Time(11,11) ->  0 Time(18,18)
Time of the route: 18min

Route for vehicle 1:
 0 Time(0,0) -> 7 Time(2,4) -> 1 Time(7,11) -> 4 Time(10,13) -> 3 Time(16,16) -> 0 Time(24,24)
Time of the route: 24min

Route for vehicle 2:
 0 Time(0,0) -> 12 Time(4,4) -> 13 Time(6,6) -> 15 Time(11,11) -> 11 Time(14,14) -> 0 Time(20,20)
Time of the route: 20min

Route for vehicle 3:
 0 Time(0,0) -> 5 Time(3,3) -> 8 Time(5,5) -> 6 Time(7,7) -> 2 Time(10,10) -> 10 Time(14,14) ->
 0 Time(20,20)
Time of the route: 20min

Total time of all routes: 82min
```

For each location on a route, `Time(a,b)` is the
[solution window](https://developers.google.com/optimization/routing/vrptw#solution-windows): the vehicle that visits the location must
do so in that time interval to stay on schedule.

As an example, take a look at the following portion of the route for vehicle 0.  

```
0 Time(0,0) -> 9 Time(2,3) -> 14 Time(7,8)
```

<br />

At location 9, the solution window is `Time(2,3)`, which means the vehicle must
arrive there between times 2 and 3. Note that the solution window is contained
in the constraint time window at that location, `(0,&nbsp;3)`, given in the
problem data. The solution window starts at time 2 because it takes 2 units of
time (the 0, 9 entry of the [time matrix](https://developers.google.com/optimization/routing/vrptw#model)) to get from the depot to
location 9.

Why can the vehicle depart location 9 anytime between 2 and 3? The reason is
that since the travel time from location 9 to location 14 is 3, if the vehicle
leaves anytime before 3, it will arrive at location 14 before time 6, which is
too early for its visit. So the vehicle has to wait somewhere, e.g., the driver
could decide to wait at location 9 until time 3 without delaying completion of
the route.

You may have noticed that some solution windows (e.g. at locations 9 and 14)
have different start and end times, but others (e.g. on routes 2 and 3) have the
same start and end time. In the former case, the vehicles can wait until the end
of the window before departing, while in the latter, they must depart as soon as
they arrive.

### Save the solution windows to a list or array

The TSP section shows how to [save the routes](https://developers.google.com/optimization/routing/tsp#get-routes)
in a solution to a list or array. For a VRPTW, you can also save the
[solution windows](https://developers.google.com/optimization/routing/vrptw#solution-windows).
The functions below save the solution windows to a list (Python) or an array (C++).  

### Python

```python
def get_cumul_data(solution, routing, dimension):
    """Get cumulative data from a dimension and store it in an array."""
    # Returns an array cumul_data whose i,j entry contains the minimum and
    # maximum of CumulVar for the dimension at the jth node on route :
    # - cumul_data[i][j][0] is the minimum.
    # - cumul_data[i][j][1] is the maximum.

    cumul_data = []
    for route_nbr in range(routing.vehicles()):
        route_data = []
        index = routing.Start(route_nbr)
        dim_var = dimension.CumulVar(index)
        route_data.append([solution.Min(dim_var), solution.Max(dim_var)])
        while not routing.IsEnd(index):
            index = solution.Value(routing.NextVar(index))
            dim_var = dimension.CumulVar(index)
            route_data.append([solution.Min(dim_var), solution.Max(dim_var)])
        cumul_data.append(route_data)
    return cumul_data
```

### C++

```c++
std::vector<std::vector<std::pair<int64_t, int64_t>>> GetCumulData(
    const Assignment& solution, const RoutingModel& routing,
    const RoutingDimension& dimension) {
  // Returns an array cumul_data, whose i, j entry is a pair containing
  // the minimum and maximum of CumulVar for the dimension.:
  // - cumul_data[i][j].first is the minimum.
  // - cumul_data[i][j].second is the maximum.
  std::vector<std::vector<std::pair<int64_t, int64_t>>> cumul_data(
      routing.vehicles());

  for (int vehicle_id = 0; vehicle_id < routing.vehicles(); ++vehicle_id) {
    int64_t index = routing.Start(vehicle_id);
    IntVar* dim_var = dimension.CumulVar(index);
    cumul_data[vehicle_id].emplace_back(solution.Min(dim_var),
                                        solution.Max(dim_var));
    while (!routing.IsEnd(index)) {
      index = solution.Value(routing.NextVar(index));
      IntVar* dim_var = dimension.CumulVar(index);
      cumul_data[vehicle_id].emplace_back(solution.Min(dim_var),
                                          solution.Max(dim_var));
    }
  }
  return cumul_data;
}
```

The functions save the minimum and maximum values of the cumulative data for any
dimension (not just time).
In the current example, these values are the lower and upper bounds of the
solution window, and the dimension passed to the function is
[`time_dimension`](https://developers.google.com/optimization/routing/vrptw#time_window_constraints).

The following functions print the solution from the
[routes](https://developers.google.com/optimization/routing/vrp#get-routes) and the cumulative data.  

### Python

```python
def print_solution(routes, cumul_data):
    """Print the solution."""
    total_time = 0
    route_str = ""
    for i, route in enumerate(routes):
        if len(route) <= 2:
            continue
        route_str += "Route " + str(i) + ":\n"
        start_time = cumul_data[i][0][0]
        end_time = cumul_data[i][0][1]
        route_str += (
            "  "
            + str(route[0])
            + " Time("
            + str(start_time)
            + ", "
            + str(end_time)
            + ")"
        )
        for j in range(1, len(route)):
            start_time = cumul_data[i][j][0]
            end_time = cumul_data[i][j][1]
            route_str += (
                " -> "
                + str(route[j])
                + " Time("
                + str(start_time)
                + ", "
                + str(end_time)
                + ")"
            )
        route_str += f"\n  Route time: {start_time}min\n\n"
        total_time += cumul_data[i][len(route) - 1][0]
    route_str += f"Total time: {total_time}min"
    print(route_str)
```

### C++

```c++
void PrintSolution(
    const std::vector<std::vector<int>> routes,
    std::vector<std::vector<std::pair<int64_t, int64_t>>> cumul_data) {
  int64_t total_time{0};
  std::ostringstream route;
  for (int vehicle_id = 0; vehicle_id < routes.size(); ++vehicle_id) {
    if (routes[vehicle_id].size() <= 2) {
      continue;
    }
    route << "\nRoute " << vehicle_id << ": \n";

    route << "  " << routes[vehicle_id][0] << " Time("
          << cumul_data[vehicle_id][0].first << ", "
          << cumul_data[vehicle_id][0].second << ") ";
    for (int j = 1; j < routes[vehicle_id].size(); ++j) {
      route << "-> " << routes[vehicle_id][j] << " Time("
            << cumul_data[vehicle_id][j].first << ", "
            << cumul_data[vehicle_id][j].second << ") ";
    }
    route << "\n  Route time: "
          << cumul_data[vehicle_id][routes[vehicle_id].size() - 1].first
          << " minutes\n";

    total_time += cumul_data[vehicle_id][routes[vehicle_id].size() - 1].first;
  }
  route << "\nTotal travel time: " << total_time << " minutes";
  LOG(INFO) << route.str();
}
```

### Complete programs

The complete programs for the vehicle routing problem with time windows are
shown below.  

### Python

```python
"""Vehicles Routing Problem (VRP) with Time Windows."""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp



def create_data_model():
    """Stores the data for the problem."""
    data = {}
    data["time_matrix"] = [
        [0, 6, 9, 8, 7, 3, 6, 2, 3, 2, 6, 6, 4, 4, 5, 9, 7],
        [6, 0, 8, 3, 2, 6, 8, 4, 8, 8, 13, 7, 5, 8, 12, 10, 14],
        [9, 8, 0, 11, 10, 6, 3, 9, 5, 8, 4, 15, 14, 13, 9, 18, 9],
        [8, 3, 11, 0, 1, 7, 10, 6, 10, 10, 14, 6, 7, 9, 14, 6, 16],
        [7, 2, 10, 1, 0, 6, 9, 4, 8, 9, 13, 4, 6, 8, 12, 8, 14],
        [3, 6, 6, 7, 6, 0, 2, 3, 2, 2, 7, 9, 7, 7, 6, 12, 8],
        [6, 8, 3, 10, 9, 2, 0, 6, 2, 5, 4, 12, 10, 10, 6, 15, 5],
        [2, 4, 9, 6, 4, 3, 6, 0, 4, 4, 8, 5, 4, 3, 7, 8, 10],
        [3, 8, 5, 10, 8, 2, 2, 4, 0, 3, 4, 9, 8, 7, 3, 13, 6],
        [2, 8, 8, 10, 9, 2, 5, 4, 3, 0, 4, 6, 5, 4, 3, 9, 5],
        [6, 13, 4, 14, 13, 7, 4, 8, 4, 4, 0, 10, 9, 8, 4, 13, 4],
        [6, 7, 15, 6, 4, 9, 12, 5, 9, 6, 10, 0, 1, 3, 7, 3, 10],
        [4, 5, 14, 7, 6, 7, 10, 4, 8, 5, 9, 1, 0, 2, 6, 4, 8],
        [4, 8, 13, 9, 8, 7, 10, 3, 7, 4, 8, 3, 2, 0, 4, 5, 6],
        [5, 12, 9, 14, 12, 6, 6, 7, 3, 3, 4, 7, 6, 4, 0, 9, 2],
        [9, 10, 18, 6, 8, 12, 15, 8, 13, 9, 13, 3, 4, 5, 9, 0, 9],
        [7, 14, 9, 16, 14, 8, 5, 10, 6, 5, 4, 10, 8, 6, 2, 9, 0],
    ]
    data["time_windows"] = [
        (0, 5),  # depot
        (7, 12),  # 1
        (10, 15),  # 2
        (16, 18),  # 3
        (10, 13),  # 4
        (0, 5),  # 5
        (5, 10),  # 6
        (0, 4),  # 7
        (5, 10),  # 8
        (0, 3),  # 9
        (10, 16),  # 10
        (10, 15),  # 11
        (0, 5),  # 12
        (5, 10),  # 13
        (7, 8),  # 14
        (10, 15),  # 15
        (11, 15),  # 16
    ]
    data["num_vehicles"] = 4
    data["depot"] = 0
    return data


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f"Objective: {solution.ObjectiveValue()}")
    time_dimension = routing.GetDimensionOrDie("Time")
    total_time = 0
    for vehicle_id in range(data["num_vehicles"]):
        if not routing.IsVehicleUsed(solution, vehicle_id):
            continue
        index = routing.Start(vehicle_id)
        plan_output = f"Route for vehicle {vehicle_id}:\n"
        while not routing.IsEnd(index):
            time_var = time_dimension.CumulVar(index)
            plan_output += (
                f"{manager.IndexToNode(index)}"
                f" Time({solution.Min(time_var)},{solution.Max(time_var)})"
                " -> "
            )
            index = solution.Value(routing.NextVar(index))
        time_var = time_dimension.CumulVar(index)
        plan_output += (
            f"{manager.IndexToNode(index)}"
            f" Time({solution.Min(time_var)},{solution.Max(time_var)})\n"
        )
        plan_output += f"Time of the route: {solution.Min(time_var)}min\n"
        print(plan_output)
        total_time += solution.Min(time_var)
    print(f"Total time of all routes: {total_time}min")


def main():
    """Solve the VRP with time windows."""
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data["time_matrix"]), data["num_vehicles"], data["depot"]
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def time_callback(from_index, to_index):
        """Returns the travel time between the two nodes."""
        # Convert from routing variable Index to time matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["time_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(time_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Time Windows constraint.
    time = "Time"
    routing.AddDimension(
        transit_callback_index,
        30,  # allow waiting time
        30,  # maximum time per vehicle
        False,  # Don't force start cumul to zero.
        time,
    )
    time_dimension = routing.GetDimensionOrDie(time)
    # Add time window constraints for each location except depot.
    for location_idx, time_window in enumerate(data["time_windows"]):
        if location_idx == data["depot"]:
            continue
        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])
    # Add time window constraints for each vehicle start node.
    depot_idx = data["depot"]
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        time_dimension.CumulVar(index).SetRange(
            data["time_windows"][depot_idx][0], data["time_windows"][depot_idx][1]
        )

    # Instantiate route start and end times to produce feasible times.
    for i in range(data["num_vehicles"]):
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.Start(i))
        )
        routing.AddVariableMinimizedByFinalizer(time_dimension.CumulVar(routing.End(i)))

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)


if __name__ == "__main__":
    main()
```

### C++

```c++
#include <cstdint>
#include <cstdlib>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

#include "ortools/base/logging.h"
#include "ortools/constraint_solver/constraint_solver.h"
#include "ortools/constraint_solver/routing.h"
#include "ortools/constraint_solver/routing_enums.pb.h"
#include "ortools/constraint_solver/routing_index_manager.h"
#include "ortools/constraint_solver/routing_parameters.h"

namespace operations_research {
struct DataModel {
  const std::vector<std::vector<int64_t>> time_matrix{
      {0, 6, 9, 8, 7, 3, 6, 2, 3, 2, 6, 6, 4, 4, 5, 9, 7},
      {6, 0, 8, 3, 2, 6, 8, 4, 8, 8, 13, 7, 5, 8, 12, 10, 14},
      {9, 8, 0, 11, 10, 6, 3, 9, 5, 8, 4, 15, 14, 13, 9, 18, 9},
      {8, 3, 11, 0, 1, 7, 10, 6, 10, 10, 14, 6, 7, 9, 14, 6, 16},
      {7, 2, 10, 1, 0, 6, 9, 4, 8, 9, 13, 4, 6, 8, 12, 8, 14},
      {3, 6, 6, 7, 6, 0, 2, 3, 2, 2, 7, 9, 7, 7, 6, 12, 8},
      {6, 8, 3, 10, 9, 2, 0, 6, 2, 5, 4, 12, 10, 10, 6, 15, 5},
      {2, 4, 9, 6, 4, 3, 6, 0, 4, 4, 8, 5, 4, 3, 7, 8, 10},
      {3, 8, 5, 10, 8, 2, 2, 4, 0, 3, 4, 9, 8, 7, 3, 13, 6},
      {2, 8, 8, 10, 9, 2, 5, 4, 3, 0, 4, 6, 5, 4, 3, 9, 5},
      {6, 13, 4, 14, 13, 7, 4, 8, 4, 4, 0, 10, 9, 8, 4, 13, 4},
      {6, 7, 15, 6, 4, 9, 12, 5, 9, 6, 10, 0, 1, 3, 7, 3, 10},
      {4, 5, 14, 7, 6, 7, 10, 4, 8, 5, 9, 1, 0, 2, 6, 4, 8},
      {4, 8, 13, 9, 8, 7, 10, 3, 7, 4, 8, 3, 2, 0, 4, 5, 6},
      {5, 12, 9, 14, 12, 6, 6, 7, 3, 3, 4, 7, 6, 4, 0, 9, 2},
      {9, 10, 18, 6, 8, 12, 15, 8, 13, 9, 13, 3, 4, 5, 9, 0, 9},
      {7, 14, 9, 16, 14, 8, 5, 10, 6, 5, 4, 10, 8, 6, 2, 9, 0},
  };
  const std::vector<std::pair<int64_t, int64_t>> time_windows{
      {0, 5},    // depot
      {7, 12},   // 1
      {10, 15},  // 2
      {16, 18},  // 3
      {10, 13},  // 4
      {0, 5},    // 5
      {5, 10},   // 6
      {0, 4},    // 7
      {5, 10},   // 8
      {0, 3},    // 9
      {10, 16},  // 10
      {10, 15},  // 11
      {0, 5},    // 12
      {5, 10},   // 13
      {7, 8},    // 14
      {10, 15},  // 15
      {11, 15},  // 16
  };
  const int num_vehicles = 4;
  const RoutingIndexManager::NodeIndex depot{0};
};

//! @brief Print the solution.
//! @param[in] data Data of the problem.
//! @param[in] manager Index manager used.
//! @param[in] routing Routing solver used.
//! @param[in] solution Solution found by the solver.
void PrintSolution(const DataModel& data, const RoutingIndexManager& manager,
                   const RoutingModel& routing, const Assignment& solution) {
  const RoutingDimension& time_dimension = routing.GetDimensionOrDie("Time");
  int64_t total_time{0};
  for (int vehicle_id = 0; vehicle_id < data.num_vehicles; ++vehicle_id) {
    if (!routing.IsVehicleUsed(solution, vehicle_id)) {
      continue;
    }
    int64_t index = routing.Start(vehicle_id);
    LOG(INFO) << "Route for vehicle " << vehicle_id << ":";
    std::ostringstream route;
    while (!routing.IsEnd(index)) {
      auto time_var = time_dimension.CumulVar(index);
      route << manager.IndexToNode(index).value() << " Time("
            << solution.Min(time_var) << ", " << solution.Max(time_var)
            << ") -> ";
      index = solution.Value(routing.NextVar(index));
    }
    auto time_var = time_dimension.CumulVar(index);
    LOG(INFO) << route.str() << manager.IndexToNode(index).value() << " Time("
              << solution.Min(time_var) << ", " << solution.Max(time_var)
              << ")";
    LOG(INFO) << "Time of the route: " << solution.Min(time_var) << "min";
    total_time += solution.Min(time_var);
  }
  LOG(INFO) << "Total time of all routes: " << total_time << "min";
  LOG(INFO) << "";
  LOG(INFO) << "Advanced usage:";
  LOG(INFO) << "Problem solved in " << routing.solver()->wall_time() << "ms";
}

void VrpTimeWindows() {
  // Instantiate the data problem.
  DataModel data;

  // Create Routing Index Manager
  RoutingIndexManager manager(data.time_matrix.size(), data.num_vehicles,
                              data.depot);

  // Create Routing Model.
  RoutingModel routing(manager);

  // Create and register a transit callback.
  const int transit_callback_index = routing.RegisterTransitCallback(
      [&data, &manager](const int64_t from_index,
                        const int64_t to_index) -> int64_t {
        // Convert from routing variable Index to time matrix NodeIndex.
        const int from_node = manager.IndexToNode(from_index).value();
        const int to_node = manager.IndexToNode(to_index).value();
        return data.time_matrix[from_node][to_node];
      });

  // Define cost of each arc.
  routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index);

  // Add Time constraint.
  const std::string time = "Time";
  routing.AddDimension(transit_callback_index,  // transit callback index
                       int64_t{30},             // allow waiting time
                       int64_t{30},             // maximum time per vehicle
                       false,  // Don't force start cumul to zero
                       time);
  const RoutingDimension& time_dimension = routing.GetDimensionOrDie(time);
  // Add time window constraints for each location except depot.
  for (int i = 1; i < data.time_windows.size(); ++i) {
    const int64_t index =
        manager.NodeToIndex(RoutingIndexManager::NodeIndex(i));
    time_dimension.CumulVar(index)->SetRange(data.time_windows[i].first,
                                             data.time_windows[i].second);
  }
  // Add time window constraints for each vehicle start node.
  for (int i = 0; i < data.num_vehicles; ++i) {
    const int64_t index = routing.Start(i);
    time_dimension.CumulVar(index)->SetRange(data.time_windows[0].first,
                                             data.time_windows[0].second);
  }

  // Instantiate route start and end times to produce feasible times.
  for (int i = 0; i < data.num_vehicles; ++i) {
    routing.AddVariableMinimizedByFinalizer(
        time_dimension.CumulVar(routing.Start(i)));
    routing.AddVariableMinimizedByFinalizer(
        time_dimension.CumulVar(routing.End(i)));
  }

  // Setting first solution heuristic.
  RoutingSearchParameters searchParameters = DefaultRoutingSearchParameters();
  searchParameters.set_first_solution_strategy(
      FirstSolutionStrategy::PATH_CHEAPEST_ARC);

  // Solve the problem.
  const Assignment* solution = routing.SolveWithParameters(searchParameters);

  // Print solution on console.
  PrintSolution(data, manager, routing, *solution);
}
}  // namespace operations_research

int main(int /*argc*/, char* /*argv*/[]) {
  operations_research::VrpTimeWindows();
  return EXIT_SUCCESS;
}
```

### Java

```java
package com.google.ortools.constraintsolver.samples;

import com.google.ortools.Loader;
import com.google.ortools.constraintsolver.Assignment;
import com.google.ortools.constraintsolver.FirstSolutionStrategy;
import com.google.ortools.constraintsolver.IntVar;
import com.google.ortools.constraintsolver.RoutingDimension;
import com.google.ortools.constraintsolver.RoutingIndexManager;
import com.google.ortools.constraintsolver.RoutingModel;
import com.google.ortools.constraintsolver.RoutingSearchParameters;
import com.google.ortools.constraintsolver.main;
import java.util.logging.Logger;

/** VRPTW. */
public class VrpTimeWindows {
  private static final Logger logger = Logger.getLogger(VrpTimeWindows.class.getName());
  static class DataModel {
    public final long[][] timeMatrix = {
        {0, 6, 9, 8, 7, 3, 6, 2, 3, 2, 6, 6, 4, 4, 5, 9, 7},
        {6, 0, 8, 3, 2, 6, 8, 4, 8, 8, 13, 7, 5, 8, 12, 10, 14},
        {9, 8, 0, 11, 10, 6, 3, 9, 5, 8, 4, 15, 14, 13, 9, 18, 9},
        {8, 3, 11, 0, 1, 7, 10, 6, 10, 10, 14, 6, 7, 9, 14, 6, 16},
        {7, 2, 10, 1, 0, 6, 9, 4, 8, 9, 13, 4, 6, 8, 12, 8, 14},
        {3, 6, 6, 7, 6, 0, 2, 3, 2, 2, 7, 9, 7, 7, 6, 12, 8},
        {6, 8, 3, 10, 9, 2, 0, 6, 2, 5, 4, 12, 10, 10, 6, 15, 5},
        {2, 4, 9, 6, 4, 3, 6, 0, 4, 4, 8, 5, 4, 3, 7, 8, 10},
        {3, 8, 5, 10, 8, 2, 2, 4, 0, 3, 4, 9, 8, 7, 3, 13, 6},
        {2, 8, 8, 10, 9, 2, 5, 4, 3, 0, 4, 6, 5, 4, 3, 9, 5},
        {6, 13, 4, 14, 13, 7, 4, 8, 4, 4, 0, 10, 9, 8, 4, 13, 4},
        {6, 7, 15, 6, 4, 9, 12, 5, 9, 6, 10, 0, 1, 3, 7, 3, 10},
        {4, 5, 14, 7, 6, 7, 10, 4, 8, 5, 9, 1, 0, 2, 6, 4, 8},
        {4, 8, 13, 9, 8, 7, 10, 3, 7, 4, 8, 3, 2, 0, 4, 5, 6},
        {5, 12, 9, 14, 12, 6, 6, 7, 3, 3, 4, 7, 6, 4, 0, 9, 2},
        {9, 10, 18, 6, 8, 12, 15, 8, 13, 9, 13, 3, 4, 5, 9, 0, 9},
        {7, 14, 9, 16, 14, 8, 5, 10, 6, 5, 4, 10, 8, 6, 2, 9, 0},
    };
    public final long[][] timeWindows = {
        {0, 5}, // depot
        {7, 12}, // 1
        {10, 15}, // 2
        {16, 18}, // 3
        {10, 13}, // 4
        {0, 5}, // 5
        {5, 10}, // 6
        {0, 4}, // 7
        {5, 10}, // 8
        {0, 3}, // 9
        {10, 16}, // 10
        {10, 15}, // 11
        {0, 5}, // 12
        {5, 10}, // 13
        {7, 8}, // 14
        {10, 15}, // 15
        {11, 15}, // 16
    };
    public final int vehicleNumber = 4;
    public final int depot = 0;
  }

  /// @brief Print the solution.
  static void printSolution(
      DataModel data, RoutingModel routing, RoutingIndexManager manager, Assignment solution) {
    // Solution cost.
    logger.info("Objective : " + solution.objectiveValue());
    // Inspect solution.
    RoutingDimension timeDimension = routing.getMutableDimension("Time");
    long totalTime = 0;
    for (int i = 0; i < data.vehicleNumber; ++i) {
      if (!routing.isVehicleUsed(solution, i)) {
        continue;
      }
      long index = routing.start(i);
      logger.info("Route for Vehicle " + i + ":");
      String route = "";
      while (!routing.isEnd(index)) {
        IntVar timeVar = timeDimension.cumulVar(index);
        route += manager.indexToNode(index) + " Time(" + solution.min(timeVar) + ","
            + solution.max(timeVar) + ") -> ";
        index = solution.value(routing.nextVar(index));
      }
      IntVar timeVar = timeDimension.cumulVar(index);
      route += manager.indexToNode(index) + " Time(" + solution.min(timeVar) + ","
          + solution.max(timeVar) + ")";
      logger.info(route);
      logger.info("Time of the route: " + solution.min(timeVar) + "min");
      totalTime += solution.min(timeVar);
    }
    logger.info("Total time of all routes: " + totalTime + "min");
  }

  public static void main(String[] args) throws Exception {
    Loader.loadNativeLibraries();
    // Instantiate the data problem.
    final DataModel data = new DataModel();

    // Create Routing Index Manager
    RoutingIndexManager manager =
        new RoutingIndexManager(data.timeMatrix.length, data.vehicleNumber, data.depot);

    // Create Routing Model.
    RoutingModel routing = new RoutingModel(manager);

    // Create and register a transit callback.
    final int transitCallbackIndex =
        routing.registerTransitCallback((long fromIndex, long toIndex) -> {
          // Convert from routing variable Index to user NodeIndex.
          int fromNode = manager.indexToNode(fromIndex);
          int toNode = manager.indexToNode(toIndex);
          return data.timeMatrix[fromNode][toNode];
        });

    // Define cost of each arc.
    routing.setArcCostEvaluatorOfAllVehicles(transitCallbackIndex);

    // Add Time constraint.
    boolean unused = routing.addDimension(transitCallbackIndex, // transit callback
        30, // allow waiting time
        30, // vehicle maximum capacities
        false, // start cumul to zero
        "Time");
    RoutingDimension timeDimension = routing.getMutableDimension("Time");
    // Add time window constraints for each location except depot.
    for (int i = 1; i < data.timeWindows.length; ++i) {
      long index = manager.nodeToIndex(i);
      timeDimension.cumulVar(index).setRange(data.timeWindows[i][0], data.timeWindows[i][1]);
    }
    // Add time window constraints for each vehicle start node.
    for (int i = 0; i < data.vehicleNumber; ++i) {
      long index = routing.start(i);
      timeDimension.cumulVar(index).setRange(data.timeWindows[0][0], data.timeWindows[0][1]);
    }

    // Instantiate route start and end times to produce feasible times.
    for (int i = 0; i < data.vehicleNumber; ++i) {
      routing.addVariableMinimizedByFinalizer(timeDimension.cumulVar(routing.start(i)));
      routing.addVariableMinimizedByFinalizer(timeDimension.cumulVar(routing.end(i)));
    }

    // Setting first solution heuristic.
    RoutingSearchParameters searchParameters =
        main.defaultRoutingSearchParameters()
            .toBuilder()
            .setFirstSolutionStrategy(FirstSolutionStrategy.Value.PATH_CHEAPEST_ARC)
            .build();

    // Solve the problem.
    Assignment solution = routing.solveWithParameters(searchParameters);

    // Print solution on console.
    printSolution(data, routing, manager, solution);
  }
}
// [END_program_part1]
```

### C#

```c#
using System;
using System.Collections.Generic;
using Google.OrTools.ConstraintSolver;

/// <summary>
///   Vehicles Routing Problem (VRP) with Time Windows.
/// </summary>
public class VrpTimeWindows
{
    class DataModel
    {
        public long[,] TimeMatrix = {
            { 0, 6, 9, 8, 7, 3, 6, 2, 3, 2, 6, 6, 4, 4, 5, 9, 7 },
            { 6, 0, 8, 3, 2, 6, 8, 4, 8, 8, 13, 7, 5, 8, 12, 10, 14 },
            { 9, 8, 0, 11, 10, 6, 3, 9, 5, 8, 4, 15, 14, 13, 9, 18, 9 },
            { 8, 3, 11, 0, 1, 7, 10, 6, 10, 10, 14, 6, 7, 9, 14, 6, 16 },
            { 7, 2, 10, 1, 0, 6, 9, 4, 8, 9, 13, 4, 6, 8, 12, 8, 14 },
            { 3, 6, 6, 7, 6, 0, 2, 3, 2, 2, 7, 9, 7, 7, 6, 12, 8 },
            { 6, 8, 3, 10, 9, 2, 0, 6, 2, 5, 4, 12, 10, 10, 6, 15, 5 },
            { 2, 4, 9, 6, 4, 3, 6, 0, 4, 4, 8, 5, 4, 3, 7, 8, 10 },
            { 3, 8, 5, 10, 8, 2, 2, 4, 0, 3, 4, 9, 8, 7, 3, 13, 6 },
            { 2, 8, 8, 10, 9, 2, 5, 4, 3, 0, 4, 6, 5, 4, 3, 9, 5 },
            { 6, 13, 4, 14, 13, 7, 4, 8, 4, 4, 0, 10, 9, 8, 4, 13, 4 },
            { 6, 7, 15, 6, 4, 9, 12, 5, 9, 6, 10, 0, 1, 3, 7, 3, 10 },
            { 4, 5, 14, 7, 6, 7, 10, 4, 8, 5, 9, 1, 0, 2, 6, 4, 8 },
            { 4, 8, 13, 9, 8, 7, 10, 3, 7, 4, 8, 3, 2, 0, 4, 5, 6 },
            { 5, 12, 9, 14, 12, 6, 6, 7, 3, 3, 4, 7, 6, 4, 0, 9, 2 },
            { 9, 10, 18, 6, 8, 12, 15, 8, 13, 9, 13, 3, 4, 5, 9, 0, 9 },
            { 7, 14, 9, 16, 14, 8, 5, 10, 6, 5, 4, 10, 8, 6, 2, 9, 0 },
        };
        public long[,] TimeWindows = {
            { 0, 5 },   // depot
            { 7, 12 },  // 1
            { 10, 15 }, // 2
            { 16, 18 }, // 3
            { 10, 13 }, // 4
            { 0, 5 },   // 5
            { 5, 10 },  // 6
            { 0, 4 },   // 7
            { 5, 10 },  // 8
            { 0, 3 },   // 9
            { 10, 16 }, // 10
            { 10, 15 }, // 11
            { 0, 5 },   // 12
            { 5, 10 },  // 13
            { 7, 8 },   // 14
            { 10, 15 }, // 15
            { 11, 15 }, // 16
        };
        public int VehicleNumber = 4;
        public int Depot = 0;
    };

    /// <summary>
    ///   Print the solution.
    /// </summary>
    static void PrintSolution(in DataModel data, in RoutingModel routing, in RoutingIndexManager manager,
                              in Assignment solution)
    {
        Console.WriteLine($"Objective {solution.ObjectiveValue()}:");

        // Inspect solution.
        RoutingDimension timeDimension = routing.GetMutableDimension("Time");
        long totalTime = 0;
        for (int i = 0; i < data.VehicleNumber; ++i)
        {
            if (!routing.IsVehicleUsed(solution, i))
            {
                continue;
            }
            Console.WriteLine("Route for Vehicle {0}:", i);
            var index = routing.Start(i);
            while (routing.IsEnd(index) == false)
            {
                var timeVar = timeDimension.CumulVar(index);
                Console.Write("{0} Time({1},{2}) -> ", manager.IndexToNode(index), solution.Min(timeVar),
                              solution.Max(timeVar));
                index = solution.Value(routing.NextVar(index));
            }
            var endTimeVar = timeDimension.CumulVar(index);
            Console.WriteLine("{0} Time({1},{2})", manager.IndexToNode(index), solution.Min(endTimeVar),
                              solution.Max(endTimeVar));
            Console.WriteLine("Time of the route: {0}min", solution.Min(endTimeVar));
            totalTime += solution.Min(endTimeVar);
        }
        Console.WriteLine("Total time of all routes: {0}min", totalTime);
    }

    public static void Main(String[] args)
    {
        // Instantiate the data problem.
        DataModel data = new DataModel();

        // Create Routing Index Manager
        RoutingIndexManager manager =
            new RoutingIndexManager(data.TimeMatrix.GetLength(0), data.VehicleNumber, data.Depot);

        // Create Routing Model.
        RoutingModel routing = new RoutingModel(manager);

        // Create and register a transit callback.
        int transitCallbackIndex = routing.RegisterTransitCallback((long fromIndex, long toIndex) =>
                                                                   {
                                                                       // Convert from routing variable Index to time
                                                                       // matrix NodeIndex.
                                                                       var fromNode = manager.IndexToNode(fromIndex);
                                                                       var toNode = manager.IndexToNode(toIndex);
                                                                       return data.TimeMatrix[fromNode, toNode];
                                                                   });

        // Define cost of each arc.
        routing.SetArcCostEvaluatorOfAllVehicles(transitCallbackIndex);

        // Add Time constraint.
        routing.AddDimension(transitCallbackIndex, // transit callback
                             30,                   // allow waiting time
                             30,                   // vehicle maximum capacities
                             false,                // start cumul to zero
                             "Time");
        RoutingDimension timeDimension = routing.GetMutableDimension("Time");
        // Add time window constraints for each location except depot.
        for (int i = 1; i < data.TimeWindows.GetLength(0); ++i)
        {
            long index = manager.NodeToIndex(i);
            timeDimension.CumulVar(index).SetRange(data.TimeWindows[i, 0], data.TimeWindows[i, 1]);
        }
        // Add time window constraints for each vehicle start node.
        for (int i = 0; i < data.VehicleNumber; ++i)
        {
            long index = routing.Start(i);
            timeDimension.CumulVar(index).SetRange(data.TimeWindows[0, 0], data.TimeWindows[0, 1]);
        }

        // Instantiate route start and end times to produce feasible times.
        for (int i = 0; i < data.VehicleNumber; ++i)
        {
            routing.AddVariableMinimizedByFinalizer(timeDimension.CumulVar(routing.Start(i)));
            routing.AddVariableMinimizedByFinalizer(timeDimension.CumulVar(routing.End(i)));
        }

        // Setting first solution heuristic.
        RoutingSearchParameters searchParameters =
            operations_research_constraint_solver.DefaultRoutingSearchParameters();
        searchParameters.FirstSolutionStrategy = FirstSolutionStrategy.Types.Value.PathCheapestArc;

        // Solve the problem.
        Assignment solution = routing.SolveWithParameters(searchParameters);

        // Print solution on console.
        PrintSolution(data, routing, manager, solution);
    }
}
```