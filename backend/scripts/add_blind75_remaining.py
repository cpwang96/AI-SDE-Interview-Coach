#!/usr/bin/env python3
"""Add remaining 43 questions to complete the Blind 75 set."""

import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'coding_questions.json')

NEW_QUESTIONS = [
    # ─── Arrays ───────────────────────────────────────────────────
    {
        "id": "maximum-product-subarray",
        "title": "Maximum Product Subarray",
        "difficulty": "medium",
        "category": "Dynamic Programming",
        "tags": ["Array", "Dynamic Programming"],
        "description": "Given an integer array `nums`, find a subarray that has the largest product, and return the product.\n\nThe test cases are generated so that the answer will fit in a 32-bit integer.",
        "examples": [
            {"input": "nums = [2,3,-2,4]", "output": "6", "explanation": "[2,3] has the largest product 6."},
            {"input": "nums = [-2,0,-1]", "output": "0", "explanation": "The result cannot be 2, because [-2,-1] is not a subarray."}
        ],
        "constraints": ["1 <= nums.length <= 2 * 10^4", "-10 <= nums[i] <= 10", "The product of any subarray of nums is guaranteed to fit in a 32-bit integer."],
        "starter_code": {
            "java": "class Solution {\n    public int maxProduct(int[] nums) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def maxProduct(self, nums: List[int]) -> int:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"nums": [2,3,-2,4]}, "expected_output": 6},
            {"input": {"nums": [-2,0,-1]}, "expected_output": 0},
            {"input": {"nums": [-2,3,-4]}, "expected_output": 24},
            {"input": {"nums": [0,2]}, "expected_output": 2},
            {"input": {"nums": [-1]}, "expected_output": -1}
        ]
    },
    {
        "id": "find-minimum-rotated-sorted-array",
        "title": "Find Minimum in Rotated Sorted Array",
        "difficulty": "medium",
        "category": "Binary Search",
        "tags": ["Array", "Binary Search"],
        "description": "Suppose an array of length `n` sorted in ascending order is rotated between 1 and n times. Given the sorted rotated array `nums` of unique elements, return the minimum element of this array.\n\nYou must write an algorithm that runs in O(log n) time.",
        "examples": [
            {"input": "nums = [3,4,5,1,2]", "output": "1", "explanation": "The original array was [1,2,3,4,5] rotated 3 times."},
            {"input": "nums = [4,5,6,7,0,1,2]", "output": "0"}
        ],
        "constraints": ["n == nums.length", "1 <= n <= 5000", "-5000 <= nums[i] <= 5000", "All the integers of nums are unique.", "nums is sorted and rotated between 1 and n times."],
        "starter_code": {
            "java": "class Solution {\n    public int findMin(int[] nums) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def findMin(self, nums: List[int]) -> int:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"nums": [3,4,5,1,2]}, "expected_output": 1},
            {"input": {"nums": [4,5,6,7,0,1,2]}, "expected_output": 0},
            {"input": {"nums": [11,13,15,17]}, "expected_output": 11},
            {"input": {"nums": [2,1]}, "expected_output": 1},
            {"input": {"nums": [1]}, "expected_output": 1}
        ]
    },
    {
        "id": "search-rotated-sorted-array",
        "title": "Search in Rotated Sorted Array",
        "difficulty": "medium",
        "category": "Binary Search",
        "tags": ["Array", "Binary Search"],
        "description": "There is an integer array `nums` sorted in ascending order (with distinct values). The array may have been rotated. Given the array `nums` and an integer `target`, return the index of `target` if it is in `nums`, or `-1` if it is not.",
        "examples": [
            {"input": "nums = [4,5,6,7,0,1,2], target = 0", "output": "4"},
            {"input": "nums = [4,5,6,7,0,1,2], target = 3", "output": "-1"},
            {"input": "nums = [1], target = 0", "output": "-1"}
        ],
        "constraints": ["1 <= nums.length <= 5000", "-10^4 <= nums[i] <= 10^4", "All values of nums are unique.", "nums is an ascending array that is possibly rotated.", "-10^4 <= target <= 10^4"],
        "starter_code": {
            "java": "class Solution {\n    public int search(int[] nums, int target) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def search(self, nums: List[int], target: int) -> int:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"nums": [4,5,6,7,0,1,2], "target": 0}, "expected_output": 4},
            {"input": {"nums": [4,5,6,7,0,1,2], "target": 3}, "expected_output": -1},
            {"input": {"nums": [1], "target": 0}, "expected_output": -1},
            {"input": {"nums": [1,3], "target": 3}, "expected_output": 1},
            {"input": {"nums": [5,1,3], "target": 5}, "expected_output": 0}
        ]
    },

    # ─── Bit Manipulation ─────────────────────────────────────────
    {
        "id": "sum-of-two-integers",
        "title": "Sum of Two Integers",
        "difficulty": "medium",
        "category": "Bit Manipulation",
        "tags": ["Math", "Bit Manipulation"],
        "description": "Given two integers `a` and `b`, return the sum of the two integers without using the operators `+` and `-`.",
        "examples": [
            {"input": "a = 1, b = 2", "output": "3"},
            {"input": "a = 2, b = 3", "output": "5"}
        ],
        "constraints": ["-1000 <= a, b <= 1000"],
        "starter_code": {
            "java": "class Solution {\n    public int getSum(int a, int b) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def getSum(self, a: int, b: int) -> int:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"a": 1, "b": 2}, "expected_output": 3},
            {"input": {"a": 2, "b": 3}, "expected_output": 5},
            {"input": {"a": -1, "b": 1}, "expected_output": 0},
            {"input": {"a": 0, "b": 0}, "expected_output": 0},
            {"input": {"a": -5, "b": 3}, "expected_output": -2}
        ]
    },
    {
        "id": "number-of-1-bits",
        "title": "Number of 1 Bits",
        "difficulty": "easy",
        "category": "Bit Manipulation",
        "tags": ["Bit Manipulation", "Divide and Conquer"],
        "description": "Write a function that takes the binary representation of a positive integer and returns the number of set bits it has (also known as the Hamming weight).",
        "examples": [
            {"input": "n = 11", "output": "3", "explanation": "11 = 1011 in binary, which has 3 set bits."},
            {"input": "n = 128", "output": "1", "explanation": "128 = 10000000 in binary, which has 1 set bit."}
        ],
        "constraints": ["1 <= n <= 2^31 - 1"],
        "starter_code": {
            "java": "class Solution {\n    public int hammingWeight(int n) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def hammingWeight(self, n: int) -> int:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"n": 11}, "expected_output": 3},
            {"input": {"n": 128}, "expected_output": 1},
            {"input": {"n": 2147483645}, "expected_output": 30},
            {"input": {"n": 1}, "expected_output": 1},
            {"input": {"n": 4294967293}, "expected_output": 31}
        ]
    },
    {
        "id": "counting-bits",
        "title": "Counting Bits",
        "difficulty": "easy",
        "category": "Bit Manipulation",
        "tags": ["Dynamic Programming", "Bit Manipulation"],
        "description": "Given an integer `n`, return an array `ans` of length `n + 1` such that for each `i` (0 <= i <= n), `ans[i]` is the number of 1's in the binary representation of `i`.",
        "examples": [
            {"input": "n = 2", "output": "[0,1,1]"},
            {"input": "n = 5", "output": "[0,1,1,2,1,2]"}
        ],
        "constraints": ["0 <= n <= 10^5"],
        "starter_code": {
            "java": "class Solution {\n    public int[] countBits(int n) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def countBits(self, n: int) -> List[int]:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"n": 2}, "expected_output": [0,1,1]},
            {"input": {"n": 5}, "expected_output": [0,1,1,2,1,2]},
            {"input": {"n": 0}, "expected_output": [0]},
            {"input": {"n": 1}, "expected_output": [0,1]},
            {"input": {"n": 8}, "expected_output": [0,1,1,2,1,2,2,3,1]}
        ]
    },
    {
        "id": "missing-number",
        "title": "Missing Number",
        "difficulty": "easy",
        "category": "Bit Manipulation",
        "tags": ["Array", "Hash Table", "Math", "Bit Manipulation", "Sorting"],
        "description": "Given an array `nums` containing `n` distinct numbers in the range `[0, n]`, return the only number in the range that is missing from the array.",
        "examples": [
            {"input": "nums = [3,0,1]", "output": "2"},
            {"input": "nums = [0,1]", "output": "2"}
        ],
        "constraints": ["n == nums.length", "1 <= n <= 10^4", "0 <= nums[i] <= n", "All the numbers of nums are unique."],
        "starter_code": {
            "java": "class Solution {\n    public int missingNumber(int[] nums) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def missingNumber(self, nums: List[int]) -> int:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"nums": [3,0,1]}, "expected_output": 2},
            {"input": {"nums": [0,1]}, "expected_output": 2},
            {"input": {"nums": [9,6,4,2,3,5,7,0,1]}, "expected_output": 8},
            {"input": {"nums": [0]}, "expected_output": 1},
            {"input": {"nums": [1]}, "expected_output": 0}
        ]
    },
    {
        "id": "reverse-bits",
        "title": "Reverse Bits",
        "difficulty": "easy",
        "category": "Bit Manipulation",
        "tags": ["Divide and Conquer", "Bit Manipulation"],
        "description": "Reverse bits of a given 32 bits unsigned integer.",
        "examples": [
            {"input": "n = 00000010100101000001111010011100", "output": "964176192", "explanation": "The input binary string 00000010100101000001111010011100 represents the unsigned integer 43261596, so return 964176192 whose binary representation is 00111001011110000010100101000000."},
            {"input": "n = 11111111111111111111111111111101", "output": "3221225471"}
        ],
        "constraints": ["The input must be a binary string of length 32"],
        "starter_code": {
            "java": "public class Solution {\n    // you need treat n as an unsigned value\n    public int reverseBits(int n) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def reverseBits(self, n: int) -> int:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"n": 43261596}, "expected_output": 964176192},
            {"input": {"n": 4294967293}, "expected_output": 3221225471},
            {"input": {"n": 0}, "expected_output": 0},
            {"input": {"n": 1}, "expected_output": 2147483648}
        ]
    },

    # ─── Dynamic Programming ──────────────────────────────────────
    {
        "id": "house-robber",
        "title": "House Robber",
        "difficulty": "medium",
        "category": "Dynamic Programming",
        "tags": ["Array", "Dynamic Programming"],
        "description": "You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed; the only constraint stopping you from robbing each of them is that adjacent houses have security systems connected and it will automatically contact the police if two adjacent houses were broken into on the same night.\n\nGiven an integer array `nums` representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police.",
        "examples": [
            {"input": "nums = [1,2,3,1]", "output": "4", "explanation": "Rob house 1 (money = 1) and then rob house 3 (money = 3). Total = 4."},
            {"input": "nums = [2,7,9,3,1]", "output": "12", "explanation": "Rob house 1, 3, and 5 for 2+9+1=12."}
        ],
        "constraints": ["1 <= nums.length <= 100", "0 <= nums[i] <= 400"],
        "starter_code": {
            "java": "class Solution {\n    public int rob(int[] nums) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def rob(self, nums: List[int]) -> int:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"nums": [1,2,3,1]}, "expected_output": 4},
            {"input": {"nums": [2,7,9,3,1]}, "expected_output": 12},
            {"input": {"nums": [1,1,1]}, "expected_output": 2},
            {"input": {"nums": [0]}, "expected_output": 0},
            {"input": {"nums": [2,1,1,2]}, "expected_output": 4}
        ]
    },
    {
        "id": "house-robber-ii",
        "title": "House Robber II",
        "difficulty": "medium",
        "category": "Dynamic Programming",
        "tags": ["Array", "Dynamic Programming"],
        "description": "All houses at this place are arranged in a circle. Given an integer array `nums` representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police (you cannot rob adjacent houses, and the first and last houses are also adjacent).",
        "examples": [
            {"input": "nums = [2,3,2]", "output": "3"},
            {"input": "nums = [1,2,3,1]", "output": "4"},
            {"input": "nums = [1,2,3]", "output": "3"}
        ],
        "constraints": ["1 <= nums.length <= 100", "0 <= nums[i] <= 1000"],
        "starter_code": {
            "java": "class Solution {\n    public int rob(int[] nums) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def rob(self, nums: List[int]) -> int:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"nums": [2,3,2]}, "expected_output": 3},
            {"input": {"nums": [1,2,3,1]}, "expected_output": 4},
            {"input": {"nums": [1,2,3]}, "expected_output": 3},
            {"input": {"nums": [1]}, "expected_output": 1},
            {"input": {"nums": [1,2]}, "expected_output": 2}
        ]
    },
    {
        "id": "decode-ways",
        "title": "Decode Ways",
        "difficulty": "medium",
        "category": "Dynamic Programming",
        "tags": ["String", "Dynamic Programming"],
        "description": "A message containing letters from A-Z can be encoded into numbers using 'A'->1, 'B'->2, ..., 'Z'->26. Given a string `s` containing only digits, return the number of ways to decode it.",
        "examples": [
            {"input": "s = \"12\"", "output": "2", "explanation": "\"12\" could be decoded as \"AB\" (1 2) or \"L\" (12)."},
            {"input": "s = \"226\"", "output": "3", "explanation": "\"226\" could be decoded as \"BZ\" (2 26), \"VF\" (22 6), or \"BBF\" (2 2 6)."},
            {"input": "s = \"06\"", "output": "0"}
        ],
        "constraints": ["1 <= s.length <= 100", "s contains only digits and may contain leading zeros."],
        "starter_code": {
            "java": "class Solution {\n    public int numDecodings(String s) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def numDecodings(self, s: str) -> int:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"s": "12"}, "expected_output": 2},
            {"input": {"s": "226"}, "expected_output": 3},
            {"input": {"s": "06"}, "expected_output": 0},
            {"input": {"s": "1"}, "expected_output": 1},
            {"input": {"s": "10"}, "expected_output": 1},
            {"input": {"s": "2611055971756562"}, "expected_output": 4}
        ]
    },
    {
        "id": "unique-paths",
        "title": "Unique Paths",
        "difficulty": "medium",
        "category": "Dynamic Programming",
        "tags": ["Math", "Dynamic Programming", "Combinatorics"],
        "description": "There is a robot on an `m x n` grid. The robot is initially located at the top-left corner. The robot tries to move to the bottom-right corner. The robot can only move either down or right at any point in time.\n\nGiven the two integers `m` and `n`, return the number of possible unique paths that the robot can take to reach the bottom-right corner.",
        "examples": [
            {"input": "m = 3, n = 7", "output": "28"},
            {"input": "m = 3, n = 2", "output": "3"}
        ],
        "constraints": ["1 <= m, n <= 100"],
        "starter_code": {
            "java": "class Solution {\n    public int uniquePaths(int m, int n) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def uniquePaths(self, m: int, n: int) -> int:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"m": 3, "n": 7}, "expected_output": 28},
            {"input": {"m": 3, "n": 2}, "expected_output": 3},
            {"input": {"m": 1, "n": 1}, "expected_output": 1},
            {"input": {"m": 7, "n": 3}, "expected_output": 28},
            {"input": {"m": 3, "n": 3}, "expected_output": 6}
        ]
    },
    {
        "id": "jump-game",
        "title": "Jump Game",
        "difficulty": "medium",
        "category": "Greedy",
        "tags": ["Array", "Dynamic Programming", "Greedy"],
        "description": "You are given an integer array `nums`. You are initially positioned at the first index and each element in the array represents your maximum jump length at that position.\n\nReturn `true` if you can reach the last index, or `false` otherwise.",
        "examples": [
            {"input": "nums = [2,3,1,1,4]", "output": "true", "explanation": "Jump 1 step from index 0 to 1, then 3 steps to the last index."},
            {"input": "nums = [3,2,1,0,4]", "output": "false", "explanation": "You will always arrive at index 3 no matter what. Its maximum jump length is 0, which makes it impossible to reach the last index."}
        ],
        "constraints": ["1 <= nums.length <= 10^4", "0 <= nums[i] <= 10^5"],
        "starter_code": {
            "java": "class Solution {\n    public boolean canJump(int[] nums) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def canJump(self, nums: List[int]) -> bool:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"nums": [2,3,1,1,4]}, "expected_output": True},
            {"input": {"nums": [3,2,1,0,4]}, "expected_output": False},
            {"input": {"nums": [0]}, "expected_output": True},
            {"input": {"nums": [1,0,0]}, "expected_output": False},
            {"input": {"nums": [2,0,0]}, "expected_output": True}
        ]
    },
    {
        "id": "longest-common-subsequence",
        "title": "Longest Common Subsequence",
        "difficulty": "medium",
        "category": "Dynamic Programming",
        "tags": ["String", "Dynamic Programming"],
        "description": "Given two strings `text1` and `text2`, return the length of their longest common subsequence. If there is no common subsequence, return `0`.\n\nA subsequence of a string is a new string generated from the original string with some characters (can be none) deleted without changing the relative order of the remaining characters.",
        "examples": [
            {"input": "text1 = \"abcde\", text2 = \"ace\"", "output": "3", "explanation": "The longest common subsequence is \"ace\" and its length is 3."},
            {"input": "text1 = \"abc\", text2 = \"abc\"", "output": "3"},
            {"input": "text1 = \"abc\", text2 = \"def\"", "output": "0"}
        ],
        "constraints": ["1 <= text1.length, text2.length <= 1000", "text1 and text2 consist of only lowercase English characters."],
        "starter_code": {
            "java": "class Solution {\n    public int longestCommonSubsequence(String text1, String text2) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def longestCommonSubsequence(self, text1: str, text2: str) -> int:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"text1": "abcde", "text2": "ace"}, "expected_output": 3},
            {"input": {"text1": "abc", "text2": "abc"}, "expected_output": 3},
            {"input": {"text1": "abc", "text2": "def"}, "expected_output": 0},
            {"input": {"text1": "bsbininm", "text2": "jmjkbkjkv"}, "expected_output": 1},
            {"input": {"text1": "hofubmnylkra", "text2": "pqhgxgdofcvs"}, "expected_output": 3}
        ]
    },

    # ─── Graph ────────────────────────────────────────────────────
    {
        "id": "clone-graph",
        "title": "Clone Graph",
        "difficulty": "medium",
        "category": "Graph",
        "tags": ["Hash Table", "Depth-First Search", "Breadth-First Search", "Graph"],
        "description": "Given a reference of a node in a connected undirected graph, return a deep copy (clone) of the graph.\n\nEach node in the graph contains a value (int) and a list (List[Node]) of its neighbors.\n\n```\nclass Node {\n    public int val;\n    public List<Node> neighbors;\n}\n```",
        "examples": [
            {"input": "adjList = [[2,4],[1,3],[2,4],[1,3]]", "output": "[[2,4],[1,3],[2,4],[1,3]]", "explanation": "There are 4 nodes in the graph. Node 1's neighbors are 2 and 4. Node 2's neighbors are 1 and 3. Etc."},
            {"input": "adjList = [[]]", "output": "[[]]"},
            {"input": "adjList = []", "output": "[]"}
        ],
        "constraints": ["The number of nodes in the graph is in the range [0, 100].", "1 <= Node.val <= 100", "Node.val is unique for each node.", "There are no repeated edges and no self-loops in the graph.", "The Graph is connected and all nodes can be visited starting from the given node."],
        "starter_code": {
            "java": "class Solution {\n    public Node cloneGraph(Node node) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"adjList": [[2,4],[1,3],[2,4],[1,3]]}, "expected_output": [[2,4],[1,3],[2,4],[1,3]]},
            {"input": {"adjList": [[]]}, "expected_output": [[]]},
            {"input": {"adjList": []}, "expected_output": []}
        ]
    },
    {
        "id": "pacific-atlantic-water-flow",
        "title": "Pacific Atlantic Water Flow",
        "difficulty": "medium",
        "category": "Graph",
        "tags": ["Array", "Depth-First Search", "Breadth-First Search", "Matrix"],
        "description": "There is an `m x n` rectangular island that borders both the Pacific Ocean and Atlantic Ocean. The Pacific Ocean touches the island's left and top edges, and the Atlantic Ocean touches the island's right and bottom edges.\n\nWater can only flow in four directions and only if the neighboring cell's height is less than or equal to the current cell's height.\n\nReturn a list of grid coordinates `result` where `result[i] = [ri, ci]` denotes that rain water can flow from cell `(ri, ci)` to both the Pacific and Atlantic oceans.",
        "examples": [
            {"input": "heights = [[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]", "output": "[[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]"},
            {"input": "heights = [[1]]", "output": "[[0,0]]"}
        ],
        "constraints": ["m == heights.length", "n == heights[r].length", "1 <= m, n <= 200", "0 <= heights[r][c] <= 10^5"],
        "starter_code": {
            "java": "class Solution {\n    public List<List<Integer>> pacificAtlantic(int[][] heights) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"heights": [[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]}, "expected_output": [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]},
            {"input": {"heights": [[1]]}, "expected_output": [[0,0]]}
        ]
    },
    {
        "id": "longest-consecutive-sequence",
        "title": "Longest Consecutive Sequence",
        "difficulty": "medium",
        "category": "Array",
        "tags": ["Array", "Hash Table", "Union Find"],
        "description": "Given an unsorted array of integers `nums`, return the length of the longest consecutive elements sequence.\n\nYou must write an algorithm that runs in O(n) time.",
        "examples": [
            {"input": "nums = [100,4,200,1,3,2]", "output": "4", "explanation": "The longest consecutive elements sequence is [1, 2, 3, 4]. Therefore its length is 4."},
            {"input": "nums = [0,3,7,2,5,8,4,6,0,1]", "output": "9"}
        ],
        "constraints": ["0 <= nums.length <= 10^5", "-10^9 <= nums[i] <= 10^9"],
        "starter_code": {
            "java": "class Solution {\n    public int longestConsecutive(int[] nums) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def longestConsecutive(self, nums: List[int]) -> int:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"nums": [100,4,200,1,3,2]}, "expected_output": 4},
            {"input": {"nums": [0,3,7,2,5,8,4,6,0,1]}, "expected_output": 9},
            {"input": {"nums": []}, "expected_output": 0},
            {"input": {"nums": [1]}, "expected_output": 1},
            {"input": {"nums": [1,2,3,4,5]}, "expected_output": 5}
        ]
    },
    {
        "id": "graph-valid-tree",
        "title": "Graph Valid Tree",
        "difficulty": "medium",
        "category": "Graph",
        "tags": ["Depth-First Search", "Breadth-First Search", "Union Find", "Graph"],
        "description": "You have a graph of `n` nodes labeled from `0` to `n - 1`. You are given an integer `n` and a list of edges where `edges[i] = [ai, bi]` indicates that there is an undirected edge between nodes `ai` and `bi` in the graph.\n\nReturn `true` if the edges of the given graph make up a valid tree, and `false` otherwise.",
        "examples": [
            {"input": "n = 5, edges = [[0,1],[0,2],[0,3],[1,4]]", "output": "true"},
            {"input": "n = 5, edges = [[0,1],[1,2],[2,3],[1,3],[1,4]]", "output": "false"}
        ],
        "constraints": ["1 <= n <= 2000", "0 <= edges.length <= 5000", "edges[i].length == 2", "0 <= ai, bi < n", "ai != bi", "There are no self-loops or repeated edges."],
        "starter_code": {
            "java": "class Solution {\n    public boolean validTree(int n, int[][] edges) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def validTree(self, n: int, edges: List[List[int]]) -> bool:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"n": 5, "edges": [[0,1],[0,2],[0,3],[1,4]]}, "expected_output": True},
            {"input": {"n": 5, "edges": [[0,1],[1,2],[2,3],[1,3],[1,4]]}, "expected_output": False},
            {"input": {"n": 1, "edges": []}, "expected_output": True},
            {"input": {"n": 2, "edges": [[0,1]]}, "expected_output": True},
            {"input": {"n": 3, "edges": [[0,1],[2,0],[1,2]]}, "expected_output": False}
        ]
    },
    {
        "id": "number-of-connected-components",
        "title": "Number of Connected Components in an Undirected Graph",
        "difficulty": "medium",
        "category": "Graph",
        "tags": ["Depth-First Search", "Breadth-First Search", "Union Find", "Graph"],
        "description": "You have a graph of `n` nodes. You are given an integer `n` and an array `edges` where `edges[i] = [ai, bi]` indicates that there is an edge between `ai` and `bi` in the graph.\n\nReturn the number of connected components in the graph.",
        "examples": [
            {"input": "n = 5, edges = [[0,1],[1,2],[3,4]]", "output": "2"},
            {"input": "n = 5, edges = [[0,1],[1,2],[2,3],[3,4]]", "output": "1"}
        ],
        "constraints": ["1 <= n <= 2000", "1 <= edges.length <= 5000", "edges[i].length == 2", "0 <= ai, bi < n", "ai != bi", "There are no repeated edges."],
        "starter_code": {
            "java": "class Solution {\n    public int countComponents(int n, int[][] edges) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def countComponents(self, n: int, edges: List[List[int]]) -> int:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"n": 5, "edges": [[0,1],[1,2],[3,4]]}, "expected_output": 2},
            {"input": {"n": 5, "edges": [[0,1],[1,2],[2,3],[3,4]]}, "expected_output": 1},
            {"input": {"n": 1, "edges": []}, "expected_output": 1},
            {"input": {"n": 3, "edges": []}, "expected_output": 3}
        ]
    },

    # ─── Intervals ────────────────────────────────────────────────
    {
        "id": "insert-interval",
        "title": "Insert Interval",
        "difficulty": "medium",
        "category": "Array",
        "tags": ["Array"],
        "description": "You are given an array of non-overlapping intervals `intervals` where `intervals[i] = [starti, endi]` represent the start and end of the `i`th interval and `intervals` is sorted in ascending order by `starti`. You are also given an interval `newInterval = [start, end]`.\n\nInsert `newInterval` into `intervals` such that `intervals` is still sorted in ascending order by `starti` and `intervals` still does not have any overlapping intervals (merge if necessary).\n\nReturn `intervals` after the insertion.",
        "examples": [
            {"input": "intervals = [[1,3],[6,9]], newInterval = [2,5]", "output": "[[1,5],[6,9]]"},
            {"input": "intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]", "output": "[[1,2],[3,10],[12,16]]"}
        ],
        "constraints": ["0 <= intervals.length <= 10^4", "intervals[i].length == 2", "0 <= starti <= endi <= 10^5", "intervals is sorted by starti in ascending order.", "newInterval.length == 2", "0 <= start <= end <= 10^5"],
        "starter_code": {
            "java": "class Solution {\n    public int[][] insert(int[][] intervals, int[] newInterval) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"intervals": [[1,3],[6,9]], "newInterval": [2,5]}, "expected_output": [[1,5],[6,9]]},
            {"input": {"intervals": [[1,2],[3,5],[6,7],[8,10],[12,16]], "newInterval": [4,8]}, "expected_output": [[1,2],[3,10],[12,16]]},
            {"input": {"intervals": [], "newInterval": [5,7]}, "expected_output": [[5,7]]},
            {"input": {"intervals": [[1,5]], "newInterval": [2,3]}, "expected_output": [[1,5]]},
            {"input": {"intervals": [[1,5]], "newInterval": [2,7]}, "expected_output": [[1,7]]}
        ]
    },
    {
        "id": "non-overlapping-intervals",
        "title": "Non-overlapping Intervals",
        "difficulty": "medium",
        "category": "Greedy",
        "tags": ["Array", "Dynamic Programming", "Greedy", "Sorting"],
        "description": "Given an array of intervals `intervals` where `intervals[i] = [starti, endi]`, return the minimum number of intervals you need to remove to make the rest of the intervals non-overlapping.",
        "examples": [
            {"input": "intervals = [[1,2],[2,3],[3,4],[1,3]]", "output": "1", "explanation": "[1,3] can be removed and the rest of the intervals are non-overlapping."},
            {"input": "intervals = [[1,2],[1,2],[1,2]]", "output": "2"},
            {"input": "intervals = [[1,2],[2,3]]", "output": "0"}
        ],
        "constraints": ["1 <= intervals.length <= 10^5", "intervals[i].length == 2", "-5 * 10^4 <= starti < endi <= 5 * 10^4"],
        "starter_code": {
            "java": "class Solution {\n    public int eraseOverlapIntervals(int[][] intervals) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"intervals": [[1,2],[2,3],[3,4],[1,3]]}, "expected_output": 1},
            {"input": {"intervals": [[1,2],[1,2],[1,2]]}, "expected_output": 2},
            {"input": {"intervals": [[1,2],[2,3]]}, "expected_output": 0},
            {"input": {"intervals": [[-52,31],[-73,-26],[82,97],[-65,-11],[-62,-49],[95,99],[58,95],[-31,49],[66,98],[-63,2],[30,47],[-40,-26]]}, "expected_output": 7}
        ]
    },
    {
        "id": "meeting-rooms",
        "title": "Meeting Rooms",
        "difficulty": "easy",
        "category": "Array",
        "tags": ["Array", "Sorting"],
        "description": "Given an array of meeting time intervals where `intervals[i] = [starti, endi]`, determine if a person could attend all meetings.",
        "examples": [
            {"input": "intervals = [[0,30],[5,10],[15,20]]", "output": "false"},
            {"input": "intervals = [[7,10],[2,4]]", "output": "true"}
        ],
        "constraints": ["0 <= intervals.length <= 10^4", "intervals[i].length == 2", "0 <= starti < endi <= 10^6"],
        "starter_code": {
            "java": "class Solution {\n    public boolean canAttendMeetings(int[][] intervals) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def canAttendMeetings(self, intervals: List[List[int]]) -> bool:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"intervals": [[0,30],[5,10],[15,20]]}, "expected_output": False},
            {"input": {"intervals": [[7,10],[2,4]]}, "expected_output": True},
            {"input": {"intervals": []}, "expected_output": True},
            {"input": {"intervals": [[1,5]]}, "expected_output": True},
            {"input": {"intervals": [[1,5],[5,10]]}, "expected_output": True}
        ]
    },
    {
        "id": "meeting-rooms-ii",
        "title": "Meeting Rooms II",
        "difficulty": "medium",
        "category": "Greedy",
        "tags": ["Array", "Two Pointers", "Greedy", "Sorting", "Heap (Priority Queue)", "Prefix Sum"],
        "description": "Given an array of meeting time intervals `intervals` where `intervals[i] = [starti, endi]`, return the minimum number of conference rooms required.",
        "examples": [
            {"input": "intervals = [[0,30],[5,10],[15,20]]", "output": "2"},
            {"input": "intervals = [[7,10],[2,4]]", "output": "1"}
        ],
        "constraints": ["1 <= intervals.length <= 10^4", "0 <= starti < endi <= 10^6"],
        "starter_code": {
            "java": "class Solution {\n    public int minMeetingRooms(int[][] intervals) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def minMeetingRooms(self, intervals: List[List[int]]) -> int:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"intervals": [[0,30],[5,10],[15,20]]}, "expected_output": 2},
            {"input": {"intervals": [[7,10],[2,4]]}, "expected_output": 1},
            {"input": {"intervals": [[1,5],[8,9],[8,9]]}, "expected_output": 2},
            {"input": {"intervals": [[1,10],[2,7],[3,19],[8,12],[10,20],[11,30]]}, "expected_output": 4}
        ]
    },

    # ─── Linked List ──────────────────────────────────────────────
    {
        "id": "merge-k-sorted-lists",
        "title": "Merge K Sorted Lists",
        "difficulty": "hard",
        "category": "Linked List",
        "tags": ["Linked List", "Divide and Conquer", "Heap (Priority Queue)", "Merge Sort"],
        "description": "You are given an array of `k` linked-lists `lists`, each linked-list is sorted in ascending order.\n\nMerge all the linked-lists into one sorted linked-list and return it.",
        "examples": [
            {"input": "lists = [[1,4,5],[1,3,4],[2,6]]", "output": "[1,1,2,3,4,4,5,6]"},
            {"input": "lists = []", "output": "[]"},
            {"input": "lists = [[]]", "output": "[]"}
        ],
        "constraints": ["k == lists.length", "0 <= k <= 10^4", "0 <= lists[i].length <= 500", "-10^4 <= lists[i][j] <= 10^4", "lists[i] is sorted in ascending order.", "The sum of lists[i].length will not exceed 10^4."],
        "starter_code": {
            "java": "class Solution {\n    public ListNode mergeKLists(ListNode[] lists) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"lists": [[1,4,5],[1,3,4],[2,6]]}, "expected_output": [1,1,2,3,4,4,5,6]},
            {"input": {"lists": []}, "expected_output": []},
            {"input": {"lists": [[]]}, "expected_output": []}
        ]
    },
    {
        "id": "remove-nth-node-from-end",
        "title": "Remove Nth Node From End of List",
        "difficulty": "medium",
        "category": "Linked List",
        "tags": ["Linked List", "Two Pointers"],
        "description": "Given the `head` of a linked list, remove the `n`th node from the end of the list and return its head.",
        "examples": [
            {"input": "head = [1,2,3,4,5], n = 2", "output": "[1,2,3,5]"},
            {"input": "head = [1], n = 1", "output": "[]"},
            {"input": "head = [1,2], n = 1", "output": "[1]"}
        ],
        "constraints": ["The number of nodes in the list is sz.", "1 <= sz <= 30", "0 <= Node.val <= 100", "1 <= n <= sz"],
        "starter_code": {
            "java": "class Solution {\n    public ListNode removeNthFromEnd(ListNode head, int n) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"head": [1,2,3,4,5], "n": 2}, "expected_output": [1,2,3,5]},
            {"input": {"head": [1], "n": 1}, "expected_output": []},
            {"input": {"head": [1,2], "n": 1}, "expected_output": [1]},
            {"input": {"head": [1,2,3], "n": 3}, "expected_output": [2,3]}
        ]
    },
    {
        "id": "reorder-list",
        "title": "Reorder List",
        "difficulty": "medium",
        "category": "Linked List",
        "tags": ["Linked List", "Two Pointers", "Stack", "Recursion"],
        "description": "You are given the head of a singly linked-list:\n```\nL0 → L1 → … → Ln - 1 → Ln\n```\nReorder it to:\n```\nL0 → Ln → L1 → Ln - 1 → L2 → Ln - 2 → …\n```\nYou may not modify the values in the list's nodes. Only nodes themselves may be changed.",
        "examples": [
            {"input": "head = [1,2,3,4]", "output": "[1,4,2,3]"},
            {"input": "head = [1,2,3,4,5]", "output": "[1,5,2,4,3]"}
        ],
        "constraints": ["The number of nodes in the list is in the range [1, 5 * 10^4].", "1 <= Node.val <= 1000"],
        "starter_code": {
            "java": "class Solution {\n    public void reorderList(ListNode head) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def reorderList(self, head: Optional[ListNode]) -> None:\n        # Do not return anything, modify head in-place instead.\n        pass"
        },
        "test_cases": [
            {"input": {"head": [1,2,3,4]}, "expected_output": [1,4,2,3]},
            {"input": {"head": [1,2,3,4,5]}, "expected_output": [1,5,2,4,3]},
            {"input": {"head": [1]}, "expected_output": [1]},
            {"input": {"head": [1,2]}, "expected_output": [1,2]}
        ]
    },

    # ─── Matrix ───────────────────────────────────────────────────
    {
        "id": "set-matrix-zeroes",
        "title": "Set Matrix Zeroes",
        "difficulty": "medium",
        "category": "Array",
        "tags": ["Array", "Hash Table", "Matrix"],
        "description": "Given an `m x n` integer matrix `matrix`, if an element is `0`, set its entire row and column to `0`'s.\n\nYou must do it in place.",
        "examples": [
            {"input": "matrix = [[1,1,1],[1,0,1],[1,1,1]]", "output": "[[1,0,1],[0,0,0],[1,0,1]]"},
            {"input": "matrix = [[0,1,2,0],[3,4,5,2],[1,3,1,5]]", "output": "[[0,0,0,0],[0,4,5,0],[0,3,1,0]]"}
        ],
        "constraints": ["m == matrix.length", "n == matrix[0].length", "1 <= m, n <= 200", "-2^31 <= matrix[i][j] <= 2^31 - 1"],
        "starter_code": {
            "java": "class Solution {\n    public void setZeroes(int[][] matrix) {\n        // Your code here (in-place)\n    }\n}",
            "python": "class Solution:\n    def setZeroes(self, matrix: List[List[int]]) -> None:\n        # Do not return anything, modify matrix in-place instead.\n        pass"
        },
        "test_cases": [
            {"input": {"matrix": [[1,1,1],[1,0,1],[1,1,1]]}, "expected_output": [[1,0,1],[0,0,0],[1,0,1]]},
            {"input": {"matrix": [[0,1,2,0],[3,4,5,2],[1,3,1,5]]}, "expected_output": [[0,0,0,0],[0,4,5,0],[0,3,1,0]]},
            {"input": {"matrix": [[1]]}, "expected_output": [[1]]},
            {"input": {"matrix": [[0]]}, "expected_output": [[0]]}
        ]
    },
    {
        "id": "spiral-matrix",
        "title": "Spiral Matrix",
        "difficulty": "medium",
        "category": "Array",
        "tags": ["Array", "Matrix", "Simulation"],
        "description": "Given an `m x n` `matrix`, return all elements of the `matrix` in spiral order.",
        "examples": [
            {"input": "matrix = [[1,2,3],[4,5,6],[7,8,9]]", "output": "[1,2,3,6,9,8,7,4,5]"},
            {"input": "matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]", "output": "[1,2,3,4,8,12,11,10,9,5,6,7]"}
        ],
        "constraints": ["m == matrix.length", "n == matrix[i].length", "1 <= m, n <= 10", "-100 <= matrix[i][j] <= 100"],
        "starter_code": {
            "java": "class Solution {\n    public List<Integer> spiralOrder(int[][] matrix) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"matrix": [[1,2,3],[4,5,6],[7,8,9]]}, "expected_output": [1,2,3,6,9,8,7,4,5]},
            {"input": {"matrix": [[1,2,3,4],[5,6,7,8],[9,10,11,12]]}, "expected_output": [1,2,3,4,8,12,11,10,9,5,6,7]},
            {"input": {"matrix": [[1]]}, "expected_output": [1]},
            {"input": {"matrix": [[1,2],[3,4]]}, "expected_output": [1,2,4,3]}
        ]
    },
    {
        "id": "word-search",
        "title": "Word Search",
        "difficulty": "medium",
        "category": "Array",
        "tags": ["Array", "Backtracking", "Matrix"],
        "description": "Given an `m x n` grid of characters `board` and a string `word`, return `true` if `word` exists in the grid.\n\nThe word can be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once.",
        "examples": [
            {"input": "board = [[\"A\",\"B\",\"C\",\"E\"],[\"S\",\"F\",\"C\",\"S\"],[\"A\",\"D\",\"E\",\"E\"]], word = \"ABCCED\"", "output": "true"},
            {"input": "board = [[\"A\",\"B\",\"C\",\"E\"],[\"S\",\"F\",\"C\",\"S\"],[\"A\",\"D\",\"E\",\"E\"]], word = \"SEE\"", "output": "true"},
            {"input": "board = [[\"A\",\"B\",\"C\",\"E\"],[\"S\",\"F\",\"C\",\"S\"],[\"A\",\"D\",\"E\",\"E\"]], word = \"ABCB\"", "output": "false"}
        ],
        "constraints": ["m == board.length", "n = board[i].length", "1 <= m, n <= 6", "1 <= word.length <= 15", "board and word consists of only lowercase and uppercase English letters."],
        "starter_code": {
            "java": "class Solution {\n    public boolean exist(char[][] board, String word) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def exist(self, board: List[List[str]], word: str) -> bool:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"board": [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "word": "ABCCED"}, "expected_output": True},
            {"input": {"board": [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "word": "SEE"}, "expected_output": True},
            {"input": {"board": [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "word": "ABCB"}, "expected_output": False},
            {"input": {"board": [["a"]], "word": "a"}, "expected_output": True}
        ]
    },

    # ─── String ───────────────────────────────────────────────────
    {
        "id": "longest-repeating-character-replacement",
        "title": "Longest Repeating Character Replacement",
        "difficulty": "medium",
        "category": "Sliding Window",
        "tags": ["Hash Table", "String", "Sliding Window"],
        "description": "You are given a string `s` and an integer `k`. You can choose any character of the string and change it to any other uppercase English character. You can perform this operation at most `k` times.\n\nReturn the length of the longest substring containing the same letter you can get after performing the above operations.",
        "examples": [
            {"input": "s = \"ABAB\", k = 2", "output": "4", "explanation": "Replace the two 'A's with two 'B's or vice versa."},
            {"input": "s = \"AABABBA\", k = 1", "output": "4", "explanation": "Replace the one 'A' in the middle with 'B' and form \"AABBBBA\". The substring \"BBBB\" has the longest repeating letters, which is 4."}
        ],
        "constraints": ["1 <= s.length <= 10^5", "s consists of only uppercase English letters.", "0 <= k <= s.length"],
        "starter_code": {
            "java": "class Solution {\n    public int characterReplacement(String s, int k) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def characterReplacement(self, s: str, k: int) -> int:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"s": "ABAB", "k": 2}, "expected_output": 4},
            {"input": {"s": "AABABBA", "k": 1}, "expected_output": 4},
            {"input": {"s": "A", "k": 0}, "expected_output": 1},
            {"input": {"s": "AAAA", "k": 0}, "expected_output": 4},
            {"input": {"s": "ABCD", "k": 0}, "expected_output": 1}
        ]
    },
    {
        "id": "valid-palindrome",
        "title": "Valid Palindrome",
        "difficulty": "easy",
        "category": "String",
        "tags": ["Two Pointers", "String"],
        "description": "A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers.\n\nGiven a string `s`, return `true` if it is a palindrome, or `false` otherwise.",
        "examples": [
            {"input": "s = \"A man, a plan, a canal: Panama\"", "output": "true"},
            {"input": "s = \"race a car\"", "output": "false"},
            {"input": "s = \" \"", "output": "true"}
        ],
        "constraints": ["1 <= s.length <= 2 * 10^5", "s consists only of printable ASCII characters."],
        "starter_code": {
            "java": "class Solution {\n    public boolean isPalindrome(String s) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def isPalindrome(self, s: str) -> bool:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"s": "A man, a plan, a canal: Panama"}, "expected_output": True},
            {"input": {"s": "race a car"}, "expected_output": False},
            {"input": {"s": " "}, "expected_output": True},
            {"input": {"s": "0P"}, "expected_output": False},
            {"input": {"s": "Was it a car or a cat I saw?"}, "expected_output": True}
        ]
    },
    {
        "id": "longest-palindromic-substring",
        "title": "Longest Palindromic Substring",
        "difficulty": "medium",
        "category": "String",
        "tags": ["Two Pointers", "String", "Dynamic Programming"],
        "description": "Given a string `s`, return the longest palindromic substring in `s`.",
        "examples": [
            {"input": "s = \"babad\"", "output": "\"bab\"", "explanation": "\"aba\" is also a valid answer."},
            {"input": "s = \"cbbd\"", "output": "\"bb\""}
        ],
        "constraints": ["1 <= s.length <= 1000", "s consist of only digits and English letters."],
        "starter_code": {
            "java": "class Solution {\n    public String longestPalindrome(String s) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def longestPalindrome(self, s: str) -> str:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"s": "babad"}, "expected_output": "bab"},
            {"input": {"s": "cbbd"}, "expected_output": "bb"},
            {"input": {"s": "a"}, "expected_output": "a"},
            {"input": {"s": "racecar"}, "expected_output": "racecar"},
            {"input": {"s": "ac"}, "expected_output": "a"}
        ]
    },
    {
        "id": "palindromic-substrings",
        "title": "Palindromic Substrings",
        "difficulty": "medium",
        "category": "String",
        "tags": ["Two Pointers", "String", "Dynamic Programming"],
        "description": "Given a string `s`, return the number of palindromic substrings in it.\n\nA string is a palindrome when it reads the same backward as forward.\n\nA substring is a contiguous sequence of characters within the string.",
        "examples": [
            {"input": "s = \"abc\"", "output": "3", "explanation": "Three palindromic strings: \"a\", \"b\", \"c\"."},
            {"input": "s = \"aaa\"", "output": "6", "explanation": "Six palindromic strings: \"a\", \"a\", \"a\", \"aa\", \"aa\", \"aaa\"."}
        ],
        "constraints": ["1 <= s.length <= 1000", "s consists of lowercase English letters."],
        "starter_code": {
            "java": "class Solution {\n    public int countSubstrings(String s) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def countSubstrings(self, s: str) -> int:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"s": "abc"}, "expected_output": 3},
            {"input": {"s": "aaa"}, "expected_output": 6},
            {"input": {"s": "a"}, "expected_output": 1},
            {"input": {"s": "aba"}, "expected_output": 4},
            {"input": {"s": "racecar"}, "expected_output": 10}
        ]
    },
    {
        "id": "encode-decode-strings",
        "title": "Encode and Decode Strings",
        "difficulty": "medium",
        "category": "String",
        "tags": ["Array", "String", "Design"],
        "description": "Design an algorithm to encode a list of strings to a single string. The encoded string is then sent over the network and is decoded back to the original list of strings.\n\nImplement the `encode` and `decode` methods:\n- `encode(strs)` – Encodes a list of strings to a single string.\n- `decode(s)` – Decodes a single string to a list of strings.",
        "examples": [
            {"input": "strs = [\"Hello\",\"World\"]", "output": "[\"Hello\",\"World\"]"},
            {"input": "strs = [\"\"]", "output": "[\"\"]"}
        ],
        "constraints": ["1 <= strs.length <= 200", "0 <= strs[i].length <= 200", "strs[i] contains any possible characters out of 256 valid ASCII characters."],
        "starter_code": {
            "java": "public class Codec {\n    public String encode(List<String> strs) {\n        // Your code here\n    }\n\n    public List<String> decode(String s) {\n        // Your code here\n    }\n}",
            "python": "class Codec:\n    def encode(self, strs: List[str]) -> str:\n        # Your code here\n        pass\n\n    def decode(self, s: str) -> List[str]:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"strs": ["Hello","World"]}, "expected_output": ["Hello","World"]},
            {"input": {"strs": [""]}, "expected_output": [""]},
            {"input": {"strs": ["lint","code","love","you"]}, "expected_output": ["lint","code","love","you"]},
            {"input": {"strs": [""]}, "expected_output": [""]}
        ]
    },

    # ─── Tree ─────────────────────────────────────────────────────
    {
        "id": "same-tree",
        "title": "Same Tree",
        "difficulty": "easy",
        "category": "Tree",
        "tags": ["Tree", "Depth-First Search", "Breadth-First Search", "Binary Tree"],
        "description": "Given the roots of two binary trees `p` and `q`, write a function to check if they are the same or not.\n\nTwo binary trees are considered the same if they are structurally identical, and the nodes have the same value.",
        "examples": [
            {"input": "p = [1,2,3], q = [1,2,3]", "output": "true"},
            {"input": "p = [1,2], q = [1,null,2]", "output": "false"},
            {"input": "p = [1,2,1], q = [1,1,2]", "output": "false"}
        ],
        "constraints": ["The number of nodes in both trees is in the range [0, 100].", "-10^4 <= Node.val <= 10^4"],
        "starter_code": {
            "java": "class Solution {\n    public boolean isSameTree(TreeNode p, TreeNode q) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"p": [1,2,3], "q": [1,2,3]}, "expected_output": True},
            {"input": {"p": [1,2], "q": [1,None,2]}, "expected_output": False},
            {"input": {"p": [1,2,1], "q": [1,1,2]}, "expected_output": False},
            {"input": {"p": [], "q": []}, "expected_output": True},
            {"input": {"p": [1], "q": [1]}, "expected_output": True}
        ]
    },
    {
        "id": "subtree-of-another-tree",
        "title": "Subtree of Another Tree",
        "difficulty": "easy",
        "category": "Tree",
        "tags": ["Tree", "Depth-First Search", "String Matching", "Binary Tree", "Hash Function"],
        "description": "Given the roots of two binary trees `root` and `subRoot`, return `true` if there is a subtree of `root` with the same structure and node values as `subRoot` and `false` otherwise.",
        "examples": [
            {"input": "root = [3,4,5,1,2], subRoot = [4,1,2]", "output": "true"},
            {"input": "root = [3,4,5,1,2,null,null,null,null,0], subRoot = [4,1,2]", "output": "false"}
        ],
        "constraints": ["The number of nodes in the root tree is in the range [1, 2000].", "The number of nodes in the subRoot tree is in the range [1, 1000].", "-10^4 <= root.val <= 10^4", "-10^4 <= subRoot.val <= 10^4"],
        "starter_code": {
            "java": "class Solution {\n    public boolean isSubtree(TreeNode root, TreeNode subRoot) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"root": [3,4,5,1,2], "subRoot": [4,1,2]}, "expected_output": True},
            {"input": {"root": [3,4,5,1,2,None,None,None,None,0], "subRoot": [4,1,2]}, "expected_output": False},
            {"input": {"root": [1,1], "subRoot": [1]}, "expected_output": True}
        ]
    },
    {
        "id": "lowest-common-ancestor-bst",
        "title": "Lowest Common Ancestor of a Binary Search Tree",
        "difficulty": "medium",
        "category": "Tree",
        "tags": ["Tree", "Depth-First Search", "Binary Search Tree", "Binary Tree"],
        "description": "Given a binary search tree (BST), find the lowest common ancestor (LCA) node of two given nodes in the BST.\n\nThe LCA is defined as the lowest node in T that has both p and q as descendants (where we allow a node to be a descendant of itself).",
        "examples": [
            {"input": "root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8", "output": "6"},
            {"input": "root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 4", "output": "2"},
            {"input": "root = [2,1], p = 2, q = 1", "output": "2"}
        ],
        "constraints": ["The number of nodes in the tree is in the range [2, 10^5].", "-10^9 <= Node.val <= 10^9", "All Node.val are unique.", "p != q", "p and q will exist in the BST."],
        "starter_code": {
            "java": "class Solution {\n    public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"root": [6,2,8,0,4,7,9,None,None,3,5], "p": 2, "q": 8}, "expected_output": 6},
            {"input": {"root": [6,2,8,0,4,7,9,None,None,3,5], "p": 2, "q": 4}, "expected_output": 2},
            {"input": {"root": [2,1], "p": 2, "q": 1}, "expected_output": 2}
        ]
    },
    {
        "id": "binary-tree-level-order-traversal",
        "title": "Binary Tree Level Order Traversal",
        "difficulty": "medium",
        "category": "Tree",
        "tags": ["Tree", "Breadth-First Search", "Binary Tree"],
        "description": "Given the `root` of a binary tree, return the level order traversal of its nodes' values (i.e., from left to right, level by level).",
        "examples": [
            {"input": "root = [3,9,20,null,null,15,7]", "output": "[[3],[9,20],[15,7]]"},
            {"input": "root = [1]", "output": "[[1]]"},
            {"input": "root = []", "output": "[]"}
        ],
        "constraints": ["The number of nodes in the tree is in the range [0, 2000].", "-1000 <= Node.val <= 1000"],
        "starter_code": {
            "java": "class Solution {\n    public List<List<Integer>> levelOrder(TreeNode root) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"root": [3,9,20,None,None,15,7]}, "expected_output": [[3],[9,20],[15,7]]},
            {"input": {"root": [1]}, "expected_output": [[1]]},
            {"input": {"root": []}, "expected_output": []},
            {"input": {"root": [1,2,3,4,5]}, "expected_output": [[1],[2,3],[4,5]]}
        ]
    },
    {
        "id": "binary-tree-max-path-sum",
        "title": "Binary Tree Maximum Path Sum",
        "difficulty": "hard",
        "category": "Tree",
        "tags": ["Dynamic Programming", "Tree", "Depth-First Search", "Binary Tree"],
        "description": "A path in a binary tree is a sequence of nodes where each pair of adjacent nodes in the sequence has an edge connecting them. A node can only appear in the sequence at most once. The path does not need to pass through the root.\n\nThe path sum of a path is the sum of the node's values in the path.\n\nGiven the `root` of a binary tree, return the maximum path sum of any non-empty path.",
        "examples": [
            {"input": "root = [1,2,3]", "output": "6", "explanation": "The optimal path is 2 -> 1 -> 3 with a path sum of 2 + 1 + 3 = 6."},
            {"input": "root = [-10,9,20,null,null,15,7]", "output": "42", "explanation": "The optimal path is 15 -> 20 -> 7 with a path sum of 15 + 20 + 7 = 42."}
        ],
        "constraints": ["The number of nodes in the tree is in the range [1, 3 * 10^4].", "-1000 <= Node.val <= 1000"],
        "starter_code": {
            "java": "class Solution {\n    public int maxPathSum(TreeNode root) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def maxPathSum(self, root: Optional[TreeNode]) -> int:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"root": [1,2,3]}, "expected_output": 6},
            {"input": {"root": [-10,9,20,None,None,15,7]}, "expected_output": 42},
            {"input": {"root": [-3]}, "expected_output": -3},
            {"input": {"root": [2,-1]}, "expected_output": 2}
        ]
    },
    {
        "id": "serialize-deserialize-binary-tree",
        "title": "Serialize and Deserialize Binary Tree",
        "difficulty": "hard",
        "category": "Tree",
        "tags": ["String", "Tree", "Depth-First Search", "Breadth-First Search", "Design", "Binary Tree"],
        "description": "Serialization is the process of converting a data structure or object into a sequence of bits so that it can be stored in a file or memory buffer, or transmitted across a network connection link to be reconstructed later in the same or another computer environment.\n\nDesign an algorithm to serialize and deserialize a binary tree. There is no restriction on how your serialization/deserialization algorithm should work. You just need to ensure that a binary tree can be serialized to a string and this string can be deserialized to the original tree structure.",
        "examples": [
            {"input": "root = [1,2,3,null,null,4,5]", "output": "[1,2,3,null,null,4,5]"}
        ],
        "constraints": ["The number of nodes in the tree is in the range [0, 10^4].", "-1000 <= Node.val <= 1000"],
        "starter_code": {
            "java": "public class Codec {\n    public String serialize(TreeNode root) {\n        // Your code here\n    }\n\n    public TreeNode deserialize(String data) {\n        // Your code here\n    }\n}",
            "python": "class Codec:\n    def serialize(self, root: TreeNode) -> str:\n        # Your code here\n        pass\n\n    def deserialize(self, data: str) -> TreeNode:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"root": [1,2,3,None,None,4,5]}, "expected_output": [1,2,3,None,None,4,5]},
            {"input": {"root": []}, "expected_output": []},
            {"input": {"root": [1]}, "expected_output": [1]}
        ]
    },
    {
        "id": "construct-binary-tree-from-preorder-inorder",
        "title": "Construct Binary Tree from Preorder and Inorder Traversal",
        "difficulty": "medium",
        "category": "Tree",
        "tags": ["Array", "Hash Table", "Divide and Conquer", "Tree", "Binary Tree"],
        "description": "Given two integer arrays `preorder` and `inorder` where `preorder` is the preorder traversal of a binary tree and `inorder` is the inorder traversal of the same tree, construct and return the binary tree.",
        "examples": [
            {"input": "preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]", "output": "[3,9,20,null,null,15,7]"},
            {"input": "preorder = [-1], inorder = [-1]", "output": "[-1]"}
        ],
        "constraints": ["1 <= preorder.length <= 3000", "inorder.length == preorder.length", "-3000 <= preorder[i], inorder[i] <= 3000", "preorder and inorder consist of unique values.", "Each value of inorder also appears in preorder.", "preorder is guaranteed to be the preorder traversal of the tree.", "inorder is guaranteed to be the inorder traversal of the tree."],
        "starter_code": {
            "java": "class Solution {\n    public TreeNode buildTree(int[] preorder, int[] inorder) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"preorder": [3,9,20,15,7], "inorder": [9,3,15,20,7]}, "expected_output": [3,9,20,None,None,15,7]},
            {"input": {"preorder": [-1], "inorder": [-1]}, "expected_output": [-1]}
        ]
    },
    {
        "id": "kth-smallest-in-bst",
        "title": "Kth Smallest Element in a BST",
        "difficulty": "medium",
        "category": "Tree",
        "tags": ["Tree", "Depth-First Search", "Binary Search Tree", "Binary Tree"],
        "description": "Given the `root` of a binary search tree, and an integer `k`, return the `k`th smallest value (1-indexed) of all the values of the nodes in the tree.",
        "examples": [
            {"input": "root = [3,1,4,null,2], k = 1", "output": "1"},
            {"input": "root = [5,3,6,2,4,null,null,1], k = 3", "output": "3"}
        ],
        "constraints": ["The number of nodes in the tree is n.", "1 <= k <= n <= 10^4", "0 <= Node.val <= 10^4"],
        "starter_code": {
            "java": "class Solution {\n    public int kthSmallest(TreeNode root, int k) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"root": [3,1,4,None,2], "k": 1}, "expected_output": 1},
            {"input": {"root": [5,3,6,2,4,None,None,1], "k": 3}, "expected_output": 3},
            {"input": {"root": [1], "k": 1}, "expected_output": 1}
        ]
    },
    {
        "id": "implement-trie",
        "title": "Implement Trie (Prefix Tree)",
        "difficulty": "medium",
        "category": "Tree",
        "tags": ["Hash Table", "String", "Design", "Trie"],
        "description": "A trie (pronounced as \"try\") or prefix tree is a tree data structure used to efficiently store and retrieve keys in a dataset of strings. There are various applications of this data structure, such as autocomplete and spellchecker.\n\nImplement the Trie class:\n- `Trie()` Initializes the trie object.\n- `void insert(String word)` Inserts the string word into the trie.\n- `boolean search(String word)` Returns true if the string word is in the trie (i.e., was inserted before), and false otherwise.\n- `boolean startsWith(String prefix)` Returns true if there is a previously inserted string word that has the prefix prefix, and false otherwise.",
        "examples": [
            {"input": "[\"Trie\",\"insert\",\"search\",\"search\",\"startsWith\",\"insert\",\"search\"] [[],[\"apple\"],[\"apple\"],[\"app\"],[\"app\"],[\"app\"],[\"app\"]]", "output": "[null,null,true,false,true,null,true]"}
        ],
        "constraints": ["1 <= word.length, prefix.length <= 2000", "word and prefix consist only of lowercase English letters.", "At most 3 * 10^4 calls in total will be made to insert, search, and startsWith."],
        "starter_code": {
            "java": "class Trie {\n    public Trie() {\n        // Your code here\n    }\n\n    public void insert(String word) {\n        // Your code here\n    }\n\n    public boolean search(String word) {\n        // Your code here\n    }\n\n    public boolean startsWith(String prefix) {\n        // Your code here\n    }\n}",
            "python": "class Trie:\n    def __init__(self):\n        # Your code here\n        pass\n\n    def insert(self, word: str) -> None:\n        # Your code here\n        pass\n\n    def search(self, word: str) -> bool:\n        # Your code here\n        pass\n\n    def startsWith(self, prefix: str) -> bool:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"operations": ["insert","search","search","startsWith","insert","search"], "args": [["apple"],["apple"],["app"],["app"],["app"],["app"]]}, "expected_output": [None,True,False,True,None,True]}
        ]
    },
    {
        "id": "add-and-search-word",
        "title": "Design Add and Search Words Data Structure",
        "difficulty": "medium",
        "category": "Tree",
        "tags": ["String", "Depth-First Search", "Design", "Trie"],
        "description": "Design a data structure that supports adding new words and finding if a string matches any previously added string.\n\nImplement the WordDictionary class:\n- `WordDictionary()` Initializes the object.\n- `void addWord(word)` Adds word to the data structure, it can be matched later.\n- `bool search(word)` Returns true if there is any string in the data structure that matches word or false otherwise. word may contain dots '.' where dots can be matched with any letter.",
        "examples": [
            {"input": "[\"WordDictionary\",\"addWord\",\"addWord\",\"addWord\",\"search\",\"search\",\"search\",\"search\"] [[],[\"bad\"],[\"dad\"],[\"mad\"],[\"pad\"],[\"bad\"],[\".ad\"],[\"b..\"]]", "output": "[null,null,null,null,false,true,true,true]"}
        ],
        "constraints": ["1 <= word.length <= 25", "word in addWord consists of lowercase English letters.", "word in search consist of '.' or lowercase English letters.", "There will be at most 2 dots in word for search queries.", "At most 10^4 calls will be made to addWord and search."],
        "starter_code": {
            "java": "class WordDictionary {\n    public WordDictionary() {\n        // Your code here\n    }\n\n    public void addWord(String word) {\n        // Your code here\n    }\n\n    public boolean search(String word) {\n        // Your code here\n    }\n}",
            "python": "class WordDictionary:\n    def __init__(self):\n        # Your code here\n        pass\n\n    def addWord(self, word: str) -> None:\n        # Your code here\n        pass\n\n    def search(self, word: str) -> bool:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"operations": ["addWord","addWord","addWord","search","search","search","search"], "args": [["bad"],["dad"],["mad"],["pad"],["bad"],[".ad"],["b.."]]}, "expected_output": [None,None,None,False,True,True,True]}
        ]
    },
    {
        "id": "word-search-ii",
        "title": "Word Search II",
        "difficulty": "hard",
        "category": "Tree",
        "tags": ["Array", "String", "Backtracking", "Trie", "Matrix"],
        "description": "Given an `m x n` board of characters and a list of strings `words`, return all words on the board.\n\nEach word must be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once in a word.",
        "examples": [
            {"input": "board = [[\"o\",\"a\",\"a\",\"n\"],[\"e\",\"t\",\"a\",\"e\"],[\"i\",\"h\",\"k\",\"r\"],[\"i\",\"f\",\"l\",\"v\"]], words = [\"oath\",\"pea\",\"eat\",\"rain\"]", "output": "[\"eat\",\"oath\"]"},
            {"input": "board = [[\"a\",\"b\"],[\"c\",\"d\"]], words = [\"abcb\"]", "output": "[]"}
        ],
        "constraints": ["m == board.length", "n == board[i].length", "1 <= m, n <= 12", "board[i][j] is a lowercase English letter.", "1 <= words.length <= 3 * 10^4", "1 <= words[i].length <= 10", "words[i] consists of lowercase English letters.", "All the strings of words are unique."],
        "starter_code": {
            "java": "class Solution {\n    public List<String> findWords(char[][] board, String[] words) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"board": [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]], "words": ["oath","pea","eat","rain"]}, "expected_output": ["eat","oath"]},
            {"input": {"board": [["a","b"],["c","d"]], "words": ["abcb"]}, "expected_output": []}
        ]
    },

    # ─── Heap ─────────────────────────────────────────────────────
    {
        "id": "top-k-frequent-elements",
        "title": "Top K Frequent Elements",
        "difficulty": "medium",
        "category": "Heap",
        "tags": ["Array", "Hash Table", "Divide and Conquer", "Sorting", "Heap (Priority Queue)", "Bucket Sort", "Counting", "Quickselect"],
        "description": "Given an integer array `nums` and an integer `k`, return the `k` most frequent elements. You may return the answer in any order.",
        "examples": [
            {"input": "nums = [1,1,1,2,2,3], k = 2", "output": "[1,2]"},
            {"input": "nums = [1], k = 1", "output": "[1]"}
        ],
        "constraints": ["1 <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4", "k is in the range [1, the number of unique elements in the array].", "It is guaranteed that the answer is unique."],
        "starter_code": {
            "java": "class Solution {\n    public int[] topKFrequent(int[] nums, int k) {\n        // Your code here\n    }\n}",
            "python": "class Solution:\n    def topKFrequent(self, nums: List[int], k: int) -> List[int]:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"nums": [1,1,1,2,2,3], "k": 2}, "expected_output": [1,2]},
            {"input": {"nums": [1], "k": 1}, "expected_output": [1]},
            {"input": {"nums": [4,1,-1,2,-1,2,3], "k": 2}, "expected_output": [-1,2]},
            {"input": {"nums": [1,2,3,4,5], "k": 3}, "expected_output": [1,2,3]}
        ]
    },
    {
        "id": "find-median-from-data-stream",
        "title": "Find Median from Data Stream",
        "difficulty": "hard",
        "category": "Heap",
        "tags": ["Two Pointers", "Design", "Sorting", "Heap (Priority Queue)", "Data Stream"],
        "description": "The median is the middle value in an ordered integer list. If the size of the list is even, there is no middle value, and the median is the mean of the two middle values.\n\nImplement the MedianFinder class:\n- `MedianFinder()` initializes the MedianFinder object.\n- `void addNum(int num)` adds the integer num from the data stream to the data structure.\n- `double findMedian()` returns the median of all elements so far. Answers within 10^-5 of the actual answer will be accepted.",
        "examples": [
            {"input": "[\"MedianFinder\",\"addNum\",\"addNum\",\"findMedian\",\"addNum\",\"findMedian\"] [[],[1],[2],[],[3],[]]", "output": "[null,null,null,1.5,null,2.0]"}
        ],
        "constraints": ["-10^5 <= num <= 10^5", "There will be at least one element in the data structure before calling findMedian.", "At most 5 * 10^4 calls will be made to addNum and findMedian."],
        "starter_code": {
            "java": "class MedianFinder {\n    public MedianFinder() {\n        // Your code here\n    }\n\n    public void addNum(int num) {\n        // Your code here\n    }\n\n    public double findMedian() {\n        // Your code here\n    }\n}",
            "python": "class MedianFinder:\n    def __init__(self):\n        # Your code here\n        pass\n\n    def addNum(self, num: int) -> None:\n        # Your code here\n        pass\n\n    def findMedian(self) -> float:\n        # Your code here\n        pass"
        },
        "test_cases": [
            {"input": {"operations": ["addNum","addNum","findMedian","addNum","findMedian"], "args": [[1],[2],[],[3],[]]}, "expected_output": [None,None,1.5,None,2.0]}
        ]
    },
]


def main():
    with open(DATA_FILE) as f:
        existing = json.load(f)

    existing_ids = {q['id'] for q in existing}
    added = 0
    skipped = 0

    for q in NEW_QUESTIONS:
        if q['id'] in existing_ids:
            print(f"  SKIP (already exists): {q['id']}")
            skipped += 1
        else:
            existing.append(q)
            existing_ids.add(q['id'])
            print(f"  ADD: {q['id']} — {q['title']}")
            added += 1

    with open(DATA_FILE, 'w') as f:
        json.dump(existing, f, indent=2)

    print(f"\nDone! Added {added} questions, skipped {skipped}. Total: {len(existing)}")


if __name__ == '__main__':
    main()
