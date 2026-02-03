"""
GRAPH STORED AS A BADLY FORMATTED JSON STRING - BECAUSE DATA STRUCTURES ARE OVERRATED

WARNING: This implementation stores a graph as a single unparsed string.
         Every operation requires full string parsing.
         O(1) lookups become O(n). BFS becomes O(n²).
         Your CPU will file a complaint with HR.

What this does:
Implements a graph data structure by storing it as a malformed JSON-like string
that gets parsed and rebuilt on every single operation.

The correct way:
    Use an adjacency list (dict of lists) or adjacency matrix.
    Store the graph in an actual data structure.
    Access neighbors in O(1) time.

The cursed way:
- Store entire graph as one string: "{ A:[B,C], B:[C], C:[] }"
- Parse the entire string on every read operation
- Rebuild the entire string on every write operation
- Turn O(1) neighbor lookup into O(n) string parsing
- Turn O(V + E) BFS into O(n²) nightmare
- Allocate new strings constantly
- Make garbage collector work overtime
- Pretend JSON doesn't have a standard format

Time Complexity:
    Proper adjacency list:
        - add_edge(): O(1)
        - neighbors(): O(1)
        - BFS: O(V + E)

    This abomination:
        - add_edge(): O(n) - parse entire graph, rebuild entire string
        - neighbors(): O(n) - parse entire graph to get one list
        - BFS: O(n²) - parse graph for EVERY node visited
        - Literally everything: O(n) minimum

Space Complexity:
    - O(n) for storage (same as normal graph)
    - O(n) temporary allocation on every operation
    - O(n) garbage created on every mutation
    - Garbage collector crying: priceless

Performance Comparison:

Normal adjacency list graph with 1,000 nodes:
    - Add edge: ~0.0001ms (hash table insert)
    - Get neighbors: ~0.0001ms (hash table lookup)
    - BFS: ~1ms (visit each node once)

This string-based graph with 1,000 nodes:
    - Add edge: ~5ms (parse entire graph, rebuild string)
    - Get neighbors: ~5ms (parse entire graph)
    - BFS: ~5000ms (parse graph 1,000 times)
    - Your CPU: filing for early retirement

Failure Modes:

1. Small Graph (10 nodes)
   - Still noticeable lag
   - Users wonder why it's slow
   - You say "it's the network"
   - It's not the network

2. Medium Graph (1,000 nodes)
   - Every operation takes milliseconds
   - BFS takes seconds
   - Users start complaining
   - You enable caching
   - Caching can't save you

3. Large Graph (1,000,000 nodes)
   - String is megabytes long
   - Parsing takes full seconds
   - BFS takes hours
   - Server runs out of memory
   - String allocation kills the heap
   - Application crashes
   - You're paged at 3 AM
   - You rewrite it properly
   - You never speak of the string graph again

4. BFS Pathological Case
   - Every node visited: parse entire graph
   - Visit 1000 nodes: parse graph 1000 times
   - Each parse: O(n)
   - Total: O(n²) where n is graph size
   - Normal BFS: O(V + E)
   - This BFS: O(V × graph_string_length)
   - Complexity theorists weeping

String Format Issues:

Not valid JSON:
    - No quotes around keys: { A:[B,C] }
    - Should be: { "A":["B","C"] }
    - json.loads() would reject it
    - You can't use standard parsers
    - You must parse it manually
    - Every. Single. Time.

No schema validation:
    - Could be: { A:[B,C,D,E,F,G] }
    - Could be: { A : [ B , C ] }
    - Could be: {A:[B,C],}
    - Could be: { A:[B,]C:[,D] }
    - Who knows? Hope the parser handles it!
    - (It probably doesn't)

Mutation Hell:

Add one edge:
    1. Parse entire graph string into dict
    2. Modify dict (this part is fast)
    3. Iterate through entire dict
    4. Build new string piece by piece
    5. Allocate memory for new string
    6. Old string becomes garbage
    7. Garbage collector activates
    8. You've done O(n) work to add one edge

Remove one edge:
    Same as above but worse because you need to:
    - Parse graph
    - Find edge in list
    - Remove it
    - Rebuild entire list
    - Rebuild entire string
    - Wonder why you chose this career

Memory Allocation Nightmare:

Every operation:
    - Allocates temporary dict: O(n) space
    - Allocates temporary lists: O(edges) space
    - Allocates new string: O(n) space
    - Old string waits for garbage collection
    - Heap fragmentation intensifies
    - Memory allocator cries
    - Cache misses everywhere

Comparison to Alternatives:

Adjacency List (normal way):
    graph = {"A": ["B", "C"], "B": ["C"], "C": []}
    neighbors = graph["A"]  # O(1)

String Graph (cursed way):
    graph = "{ A:[B,C], B:[C], C:[] }"
    neighbors = parse_entire_graph(graph)["A"]  # O(n)

Adjacency Matrix:
    graph = [[0,1,1], [0,0,1], [0,0,0]]
    neighbors = [i for i, x in enumerate(graph[0]) if x]  # O(V)

String Graph:
    Still worse. Parsing beats everything.
    Life is bad. But ut can get worse.

Educational Value:

Anti-Patterns Demonstrated:
1. Treating serialized data as runtime format
2. Parsing on every access instead of once at load
3. Rebuilding everything instead of updating in place
4. String manipulation instead of pointer updates
5. No separation between storage and computation
6. Choosing text processing over data structures
7. Making the computer do human-readable formatting constantly

P.S:
I could have used a dict[str, list[str]] like a normal person.
Instead I chose to store it as a string and parse it constantly.
The string isn't even valid JSON.
I have to write a custom parser.
The parser runs on every operation.
This is not a feature.
This is performance self-harm.

What We Learned:

Data structures exist for a reason.
Parsing is expensive.
Strings are for humans, not computers.
Runtime representation ≠ serialization format.
O(1) is better than O(n).
Your CPU has feelings too.

Final Thoughts:

This implementation proves that you can make any algorithm slower
by adding unnecessary parsing and serialization steps.

Author Note: I'll let the world... or in this case your computer.... or laptop....
"""

from collections import deque


class GraphAsBadJSON:
    """
    A graph stored as a badly formatted JSON-like string.

    This is the worst possible way to represent a graph in memory, guaranteeing:
    - O(n) parsing overhead on every operation
    - Constant string allocation and garbage collection
    - O(n²) complexity for simple graph traversals
    - Your CPU questioning its life choices

    Format:
        "{ A:[B,C], B:[C], C:[] }"

    Problems:
    - Not valid JSON (no quotes around keys/values)
    - No schema validation
    - No type safety
    - No guarantees about format consistency
    - Requires full parse on every single operation
    - Requires full rebuild on every mutation
    - String allocations everywhere
    - Garbage collector working overtime

    Performance:
    - add_edge(): O(n) - parse graph, modify, rebuild string
    - neighbors(): O(n) - parse entire graph to return one list
    - bfs(): O(n²) - parse graph for every node visited
    - Everything: O(n) minimum, usually worse

    Attributes:
        _graph: The entire graph as a single unparsed string
                This string is rebuilt on every mutation
                This string is parsed on every read
                This string brings suffering
    """

    def __init__(self, data: str = "{ }") -> None:
        """
        Initialize graph from a string.

        Args:
            data: Graph in cursed string format

        Notes:
            The entire graph is stored as one string.
            One string to rule them all.
            One string to parse constantly.
            Brackets doing unpaid labor.
            Commas working overtime.
        """
        self._graph = data

    def _parse(self) -> dict[str, list[str]]:
        """
        Parse the graph string into a temporary adjacency list.

        This function is called on EVERY SINGLE OPERATION.
        Read operation? Parse the graph.
        Write operation? Parse the graph.
        Just checking if a node exists? Parse the entire graph.

        Steps:
        1. Strip outer braces
        2. Split nodes by comma and bracket
        3. Split edges manually (because we didn't use real JSON)
        4. Build dict
        5. Return it
        6. Watch it get immediately discarded after use
        7. Repeat on next operation

        Time Complexity: O(n) where n is length of graph string
        Space Complexity: O(n) temporary allocation
        Garbage Generated: O(n) every single call
        CPU Happiness: O(0)
        My Sadistic nature: ;)

        Returns:
            Temporary adjacency list that will be thrown away momentarily

        Notes:
            In a normal graph implementation, this dict would BE the graph.
            Here, it's a temporary structure we build and destroy constantly.
            This is like demolishing and rebuilding your house every time
            you want to check if you have milk in the fridge.
        """
        result: dict[str, list[str]] = {}

        content = self._graph.strip().strip("{}").strip()
        if not content:
            return result

        # Split by closing bracket + comma to separate nodes
        # This is fragile and assumes format is correct
        # Spoiler: format is never correct
        nodes = content.split("],")

        for node in nodes:
            node = node.strip()
            if not node.endswith("]"):
                node += "]"

            # Parse "A:[B,C]" into name="A", edges=["B","C"]
            # Assume format is correct (it isn't)
            name, edges = node.split(":[", 1)
            name = name.strip()
            edges = edges.strip("]")

            if edges:
                result[name] = [e.strip() for e in edges.split(",")]
            else:
                result[name] = []

        return result

    def _save(self, graph: dict[str, list[str]]) -> None:
        """
        Serialize adjacency list back into cursed string format.

        This function is called on EVERY MUTATION.
        Add one edge? Rebuild entire string.
        Remove one edge? Rebuild entire string.
        Update anything? Rebuild entire string.

        Process:
        1. Iterate through every node
        2. Format each node as "A:[B,C]"
        3. Join them with commas
        4. Wrap in braces
        5. Allocate new string
        6. Old string becomes garbage
        7. Garbage collector sighs heavily

        Time Complexity: O(n) to iterate and build string
        Space Complexity: O(n) new string allocation
        Old String Fate: Garbage
        Heap Fragmentation: Yes

        Args:
            graph: The adjacency list to serialize

        Notes:
            We're throwing away a perfectly good data structure
            to rebuild a string that we'll just parse again later.
            This is like printing out your spreadsheet, filing it,
            then re-typing it every time you need to look at it.
        """
        parts = []
        for node, edges in graph.items():
            parts.append(f"{node}:[{','.join(edges)}]")
        self._graph = "{ " + ", ".join(parts) + " }"

    def add_edge(self, src: str, dst: str) -> None:
        """
        Add an edge to the graph.

        What should happen:
            graph[src].append(dst)  # O(1)

        What actually happens:
            1. Parse entire graph string into dict - O(n)
            2. Modify dict - O(1)
            3. Rebuild entire graph string - O(n)
            4. Allocate new string - O(n)
            5. Old string becomes garbage - O(sadness)

        Args:
            src: Source node
            dst: Destination node

        Time Complexity: O(n) where n is size of entire graph
        What It Should Be: O(1)
        Performance Ratio: n times slower than necessary

        Notes:
            Adding one edge requires processing the entire graph.
            With a normal adjacency list, this would be one list append.
            Instead, we parse everything, rebuild everything, allocate everything.
            The CPU is not having a good time.
        """
        graph = self._parse()  # O(n): Parse entire graph

        if src not in graph:
            graph[src] = []

        graph[src].append(dst)  # O(1): The only fast part
        self._save(graph)  # O(n): Rebuild entire string

    def neighbors(self, node: str) -> list[str]:
        """
        Get neighbors of a node.

        What should happen:
            return graph[node]  # O(1)

        What actually happens:
            1. Parse entire graph string - O(n)
            2. Look up node in temporary dict - O(1)
            3. Return list - O(1)
            4. Discard temporary dict - O(n) garbage

        Args:
            node: Node to get neighbors for

        Returns:
            List of neighbor nodes

        Time Complexity: O(n) for what should be O(1)
        Efficiency: 1/n
        CPU Satisfaction: 0/10

        Notes:
            We parse the entire graph to return one list.
            If the graph has 1,000,000 nodes and you want neighbors of one,
            we still parse all 1,000,000 nodes.
            Every. Single. Time. MUAHAHAHAHA!!
        """
        graph = self._parse()  # Parse entire graph to get one list
        return graph.get(node, [])

    def bfs(self, start: str) -> list[str]:
        """
        Breadth-first search traversal.

        Normal BFS complexity: O(V + E)
            - Visit each vertex once
            - Check each edge once
            - Use adjacency list for O(1) neighbor lookup

        This BFS complexity: O(V × n) where n is graph string length
            - Visit each vertex once
            - For each vertex, parse entire graph - O(n)
            - Total: O(V × n) which approaches O(n²)

        Args:
            start: Starting node

        Returns:
            List of nodes in BFS order

        Time Complexity: O(n²) for what should be O(V + E)
        Performance: Insulting
        CPU Usage: Maximum
        Garbage Generated: O(V × n)

        Process:
        1. Start BFS
        2. Visit node A
        3. Parse entire graph to get A's neighbors - O(n)
        4. Visit node B
        5. Parse entire graph to get B's neighbors - O(n)
        6. Repeat for every node
        7. Total: Visit V nodes × parse graph each time = O(V × n)

        Notes:
            Every single loop iteration parses the entire graph.
            We could parse once and reuse the adjacency list.
            But that would require using a data structure.
        """
        visited = set()
        order = []
        queue = deque([start])

        while queue:
            node = queue.popleft()
            if node in visited:
                continue

            visited.add(node)
            order.append(node)

            # Here's where the magic happens:
            # self.neighbors() parses the ENTIRE graph
            # This happens for EVERY node visited
            # If we visit 1000 nodes, we parse the graph 1000 times
            # Normal BFS: parse once, traverse graph
            # This BFS: parse repeatedly, suffer constantly
            for neighbor in self.neighbors(node):  # O(n) parsing happens here
                if neighbor not in visited:
                    queue.append(neighbor) # Yes. Just Yes

        return order

    def __str__(self) -> str:
        """
        Return raw graph string.

        This is the only fast operation because we're already storing
        everything as a string. Ironically, the one thing we optimize for
        is the thing nobody needs to be fast.

        Returns:
            The raw graph string in all its malformed glory
        """
        return self._graph


def main() -> None:
    """
    Demonstrate the horror of string-based graph storage.

    Watch as simple operations become expensive.
    Watch as BFS parses the graph repeatedly.
    Watch as the CPU usage climbs.
    Watch as your faith in data structures is restored.
    """
    print("Graph as Badly Formatted JSON String")

    graph = GraphAsBadJSON()

    print("\nAdding edges (each addition reparses and rebuilds graph):")
    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "C")
    graph.add_edge("C", "D")
    print("  [4 edges added, graph rebuilt 4 times]")

    print("\nRaw graph storage:")
    print(f"  {graph}")

    print("\nNeighbors of A (full parse happens here):")
    print(f"  {graph.neighbors('A')}")
    print("  [Graph parsed once to return 2 neighbors]")

    print("\nBFS traversal from A (parses graph repeatedly):")
    result = graph.bfs("A")
    print(f"  {result}")
    print(f"  [Graph parsed {len(result)} times - once per node visited]")

    print("\nPerformance Analysis:")
    print("  Normal adjacency list BFS: O(V + E)")
    print("  This string-based BFS: O(V × string_length)")
    print("  For 1000 nodes: ~1000x slower than necessary")

    print("\nConclusion:")
    print("  The graph is a string.")
    print("  The string is parsed constantly.")
    print("  The CPU is tired.")
    print("  The garbage collector is overwhelmed.")
    print("  Use adjacency lists.")
    print("  Please.")


if __name__ == "__main__":
    main()