"""
Add the remaining 43 Blind 75 questions to reach 75 total.
Each question has: description, examples, constraints, starter_code (python/js/java),
test_cases (8-10 each), tags, companies, frequency, category.
"""
import json
import os

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "coding_questions.json")

NEW_QUESTIONS = [
    # --- Arrays & Hashing ---
    {
        "id": "top-k-frequent-elements",
        "title": "Top K Frequent Elements",
        "difficulty": "medium",
        "description": "Given an integer array `nums` and an integer `k`, return the `k` most frequent elements. You may return the answer in any order.",
        "examples": [
            {"input": "nums = [1,1,1,2,2,3], k = 2", "output": "[1,2]", "explanation": ""},
            {"input": "nums = [1], k = 1", "output": "[1]", "explanation": ""}
        ],
        "constraints": ["1 <= nums.length <= 10^5", "k is in the range [1, number of unique elements]", "Answer is guaranteed to be unique"],
        "starter_code": {
            "python": "def top_k_frequent(nums: list[int], k: int) -> list[int]:\n    # Your code here\n    pass",
            "javascript": "function topKFrequent(nums, k) {\n    // Your code here\n}",
            "java": "import java.util.*;\n\npublic class Solution {\n    public static int[] topKFrequent(int[] nums, int k) {\n        // Your code here\n        return new int[]{};\n    }\n\n    public static void main(String[] args) {\n        System.out.println(Arrays.toString(topKFrequent(new int[]{1,1,1,2,2,3}, 2)));\n    }\n}"
        },
        "test_cases": [
            {"input": {"nums": [1,1,1,2,2,3], "k": 2}, "expected": [1,2]},
            {"input": {"nums": [1], "k": 1}, "expected": [1]},
            {"input": {"nums": [1,2], "k": 2}, "expected": [1,2]},
            {"input": {"nums": [4,4,4,4,1,1,2,2,2,3], "k": 2}, "expected": [4,2]},
            {"input": {"nums": [3,3,3,1,1,2], "k": 1}, "expected": [3]},
            {"input": {"nums": [5,5,5,5,5], "k": 1}, "expected": [5]},
            {"input": {"nums": [1,2,3,4,5], "k": 5}, "expected": [1,2,3,4,5]},
            {"input": {"nums": [-1,-1,2,2,3], "k": 2}, "expected": [-1,2]}
        ],
        "tags": ["array", "hash-table", "heap", "sorting"],
        "companies": ["amazon", "google", "meta"],
        "frequency": "high",
        "category": "blind75"
    },
    {
        "id": "encode-decode-strings",
        "title": "Encode and Decode Strings",
        "difficulty": "medium",
        "description": "Design an algorithm to encode a list of strings to a single string. The encoded string is then decoded back to the original list of strings.\n\nImplement `encode` and `decode` functions.",
        "examples": [
            {"input": 'strs = ["lint","code","love","you"]', "output": '["lint","code","love","you"]', "explanation": "One possible encode method: '4#lint4#code4#love3#you'"},
            {"input": 'strs = ["we","say",":","yes"]', "output": '["we","say",":","yes"]', "explanation": ""}
        ],
        "constraints": ["0 <= strs.length <= 200", "0 <= strs[i].length <= 200", "strs[i] contains any possible characters"],
        "starter_code": {
            "python": "def encode(strs: list[str]) -> str:\n    # Your code here\n    pass\n\ndef decode(s: str) -> list[str]:\n    # Your code here\n    pass",
            "javascript": "function encode(strs) {\n    // Your code here\n}\n\nfunction decode(s) {\n    // Your code here\n}",
            "java": "import java.util.*;\n\npublic class Solution {\n    public static String encode(List<String> strs) {\n        // Your code here\n        return \"\";\n    }\n\n    public static List<String> decode(String s) {\n        // Your code here\n        return new ArrayList<>();\n    }\n\n    public static void main(String[] args) {\n        List<String> input = Arrays.asList(\"lint\",\"code\",\"love\",\"you\");\n        System.out.println(decode(encode(input)));\n    }\n}"
        },
        "test_cases": [
            {"input": {"strs": ["lint","code","love","you"]}, "expected": ["lint","code","love","you"]},
            {"input": {"strs": ["we","say",":","yes"]}, "expected": ["we","say",":","yes"]},
            {"input": {"strs": []}, "expected": []},
            {"input": {"strs": [""]}, "expected": [""]},
            {"input": {"strs": ["",""]}, "expected": ["",""]},
            {"input": {"strs": ["a"]}, "expected": ["a"]},
            {"input": {"strs": ["hello world"]}, "expected": ["hello world"]},
            {"input": {"strs": ["#","##","###"]}, "expected": ["#","##","###"]}
        ],
        "tags": ["string", "design"],
        "companies": ["google", "meta"],
        "frequency": "medium",
        "category": "blind75"
    },
    {
        "id": "longest-consecutive-sequence",
        "title": "Longest Consecutive Sequence",
        "difficulty": "medium",
        "description": "Given an unsorted array of integers `nums`, return the length of the longest consecutive elements sequence.\n\nYou must write an algorithm that runs in `O(n)` time.",
        "examples": [
            {"input": "nums = [100,4,200,1,3,2]", "output": "4", "explanation": "The longest consecutive sequence is [1, 2, 3, 4]. Therefore its length is 4."},
            {"input": "nums = [0,3,7,2,5,8,4,6,0,1]", "output": "9", "explanation": ""}
        ],
        "constraints": ["0 <= nums.length <= 10^5", "-10^9 <= nums[i] <= 10^9"],
        "starter_code": {
            "python": "def longest_consecutive(nums: list[int]) -> int:\n    # Your code here\n    pass",
            "javascript": "function longestConsecutive(nums) {\n    // Your code here\n}",
            "java": "import java.util.*;\n\npublic class Solution {\n    public static int longestConsecutive(int[] nums) {\n        // Your code here\n        return 0;\n    }\n\n    public static void main(String[] args) {\n        System.out.println(longestConsecutive(new int[]{100,4,200,1,3,2}));\n    }\n}"
        },
        "test_cases": [
            {"input": {"nums": [100,4,200,1,3,2]}, "expected": 4},
            {"input": {"nums": [0,3,7,2,5,8,4,6,0,1]}, "expected": 9},
            {"input": {"nums": []}, "expected": 0},
            {"input": {"nums": [1]}, "expected": 1},
            {"input": {"nums": [1,2,3,4,5]}, "expected": 5},
            {"input": {"nums": [5,4,3,2,1]}, "expected": 5},
            {"input": {"nums": [1,3,5,7]}, "expected": 1},
            {"input": {"nums": [0,0,0]}, "expected": 1},
            {"input": {"nums": [-1,0,1,2]}, "expected": 4},
            {"input": {"nums": [9,1,4,7,3,-1,0,5,8,-1,6]}, "expected": 7}
        ],
        "tags": ["array", "hash-table", "union-find"],
        "companies": ["google", "amazon", "meta"],
        "frequency": "high",
        "category": "blind75"
    },
    # --- Two Pointers ---
    {
        "id": "valid-palindrome",
        "title": "Valid Palindrome",
        "difficulty": "easy",
        "description": "A phrase is a **palindrome** if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward.\n\nGiven a string `s`, return `true` if it is a palindrome, or `false` otherwise.",
        "examples": [
            {"input": 's = "A man, a plan, a canal: Panama"', "output": "true", "explanation": "'amanaplanacanalpanama' is a palindrome."},
            {"input": 's = "race a car"', "output": "false", "explanation": "'raceacar' is not a palindrome."}
        ],
        "constraints": ["1 <= s.length <= 2 * 10^5", "s consists only of printable ASCII characters"],
        "starter_code": {
            "python": "def is_palindrome(s: str) -> bool:\n    # Your code here\n    pass",
            "javascript": "function isPalindrome(s) {\n    // Your code here\n}",
            "java": "public class Solution {\n    public static boolean isPalindrome(String s) {\n        // Your code here\n        return false;\n    }\n\n    public static void main(String[] args) {\n        System.out.println(isPalindrome(\"A man, a plan, a canal: Panama\"));\n    }\n}"
        },
        "test_cases": [
            {"input": {"s": "A man, a plan, a canal: Panama"}, "expected": True},
            {"input": {"s": "race a car"}, "expected": False},
            {"input": {"s": " "}, "expected": True},
            {"input": {"s": "a"}, "expected": True},
            {"input": {"s": "ab"}, "expected": False},
            {"input": {"s": "aa"}, "expected": True},
            {"input": {"s": ".,"}, "expected": True},
            {"input": {"s": "0P"}, "expected": False},
            {"input": {"s": "Was it a car or a cat I saw?"}, "expected": True},
            {"input": {"s": "No lemon, no melon"}, "expected": True}
        ],
        "tags": ["string", "two-pointers"],
        "companies": ["amazon", "meta", "microsoft"],
        "frequency": "high",
        "category": "blind75"
    },
    # --- Stacks ---
    {
        "id": "min-stack",
        "title": "Min Stack",
        "difficulty": "medium",
        "description": "Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.\n\nImplement the `MinStack` class:\n- `MinStack()` initializes the stack object.\n- `void push(int val)` pushes the element val onto the stack.\n- `void pop()` removes the element on the top of the stack.\n- `int top()` gets the top element of the stack.\n- `int getMin()` retrieves the minimum element in the stack.",
        "examples": [
            {"input": 'push(-2), push(0), push(-3), getMin(), pop(), top(), getMin()', "output": "[-3, 0, -2]", "explanation": ""}
        ],
        "constraints": ["-2^31 <= val <= 2^31 - 1", "Methods pop, top, getMin will always be called on non-empty stacks", "At most 3 * 10^4 calls will be made"],
        "starter_code": {
            "python": "class MinStack:\n    def __init__(self):\n        # Your code here\n        pass\n\n    def push(self, val: int) -> None:\n        pass\n\n    def pop(self) -> None:\n        pass\n\n    def top(self) -> int:\n        pass\n\n    def getMin(self) -> int:\n        pass",
            "javascript": "class MinStack {\n    constructor() {\n        // Your code here\n    }\n\n    push(val) {\n    }\n\n    pop() {\n    }\n\n    top() {\n    }\n\n    getMin() {\n    }\n}",
            "java": "import java.util.*;\n\npublic class Solution {\n    static Stack<int[]> stack = new Stack<>();\n\n    public static void push(int val) {\n        // Your code here\n    }\n\n    public static void pop() {\n        // Your code here\n    }\n\n    public static int top() {\n        // Your code here\n        return 0;\n    }\n\n    public static int getMin() {\n        // Your code here\n        return 0;\n    }\n\n    public static void main(String[] args) {\n        push(-2); push(0); push(-3);\n        System.out.println(getMin());\n        pop();\n        System.out.println(top());\n        System.out.println(getMin());\n    }\n}"
        },
        "test_cases": [],
        "tags": ["stack", "design"],
        "companies": ["amazon", "google", "microsoft"],
        "frequency": "medium",
        "category": "blind75"
    },
    # --- Sliding Window ---
    {
        "id": "longest-repeating-character-replacement",
        "title": "Longest Repeating Character Replacement",
        "difficulty": "medium",
        "description": "You are given a string `s` and an integer `k`. You can choose any character of the string and change it to any other uppercase English letter. You can perform this operation at most `k` times.\n\nReturn the length of the longest substring containing the same letter you can get after performing the above operations.",
        "examples": [
            {"input": 's = "ABAB", k = 2', "output": "4", "explanation": "Replace the two 'A's with two 'B's or vice versa."},
            {"input": 's = "AABABBA", k = 1', "output": "4", "explanation": "Replace the one 'A' in the middle with 'B' and form 'AABBBBA'. The substring 'BBBB' has the longest repeating letters, which is 4."}
        ],
        "constraints": ["1 <= s.length <= 10^5", "s consists of only uppercase English letters", "0 <= k <= s.length"],
        "starter_code": {
            "python": "def character_replacement(s: str, k: int) -> int:\n    # Your code here\n    pass",
            "javascript": "function characterReplacement(s, k) {\n    // Your code here\n}",
            "java": "public class Solution {\n    public static int characterReplacement(String s, int k) {\n        // Your code here\n        return 0;\n    }\n\n    public static void main(String[] args) {\n        System.out.println(characterReplacement(\"ABAB\", 2));\n        System.out.println(characterReplacement(\"AABABBA\", 1));\n    }\n}"
        },
        "test_cases": [
            {"input": {"s": "ABAB", "k": 2}, "expected": 4},
            {"input": {"s": "AABABBA", "k": 1}, "expected": 4},
            {"input": {"s": "AAAA", "k": 0}, "expected": 4},
            {"input": {"s": "ABCD", "k": 0}, "expected": 1},
            {"input": {"s": "ABCD", "k": 2}, "expected": 3},
            {"input": {"s": "A", "k": 0}, "expected": 1},
            {"input": {"s": "ABBB", "k": 2}, "expected": 4},
            {"input": {"s": "AAAB", "k": 0}, "expected": 3},
            {"input": {"s": "ABAA", "k": 1}, "expected": 4}
        ],
        "tags": ["string", "sliding-window", "hash-table"],
        "companies": ["google", "amazon"],
        "frequency": "medium",
        "category": "blind75"
    },
    {
        "id": "permutation-in-string",
        "title": "Permutation in String",
        "difficulty": "medium",
        "description": "Given two strings `s1` and `s2`, return `true` if `s2` contains a permutation of `s1`, or `false` otherwise.\n\nIn other words, return `true` if one of `s1`'s permutations is the substring of `s2`.",
        "examples": [
            {"input": 's1 = "ab", s2 = "eidbaooo"', "output": "true", "explanation": "s2 contains one permutation of s1 ('ba')."},
            {"input": 's1 = "ab", s2 = "eidboaoo"', "output": "false", "explanation": ""}
        ],
        "constraints": ["1 <= s1.length, s2.length <= 10^4", "s1 and s2 consist of lowercase English letters"],
        "starter_code": {
            "python": "def check_inclusion(s1: str, s2: str) -> bool:\n    # Your code here\n    pass",
            "javascript": "function checkInclusion(s1, s2) {\n    // Your code here\n}",
            "java": "public class Solution {\n    public static boolean checkInclusion(String s1, String s2) {\n        // Your code here\n        return false;\n    }\n\n    public static void main(String[] args) {\n        System.out.println(checkInclusion(\"ab\", \"eidbaooo\"));\n    }\n}"
        },
        "test_cases": [
            {"input": {"s1": "ab", "s2": "eidbaooo"}, "expected": True},
            {"input": {"s1": "ab", "s2": "eidboaoo"}, "expected": False},
            {"input": {"s1": "a", "s2": "a"}, "expected": True},
            {"input": {"s1": "ab", "s2": "a"}, "expected": False},
            {"input": {"s1": "adc", "s2": "dcda"}, "expected": True},
            {"input": {"s1": "abc", "s2": "bbbca"}, "expected": True},
            {"input": {"s1": "hello", "s2": "ooolleoooleh"}, "expected": False},
            {"input": {"s1": "ab", "s2": "ab"}, "expected": True},
            {"input": {"s1": "abc", "s2": "ccccbbbbaaaa"}, "expected": False}
        ],
        "tags": ["string", "sliding-window", "hash-table", "two-pointers"],
        "companies": ["microsoft", "amazon"],
        "frequency": "medium",
        "category": "blind75"
    },
    # --- Binary Search ---
    {
        "id": "search-in-rotated-sorted-array",
        "title": "Search in Rotated Sorted Array",
        "difficulty": "medium",
        "description": "There is an integer array `nums` sorted in ascending order (with distinct values). Prior to being passed to your function, `nums` is possibly rotated at an unknown pivot index.\n\nGiven the array `nums` after the possible rotation and an integer `target`, return the index of `target` if it is in `nums`, or `-1` if it is not in `nums`.\n\nYou must write an algorithm with `O(log n)` runtime complexity.",
        "examples": [
            {"input": "nums = [4,5,6,7,0,1,2], target = 0", "output": "4", "explanation": ""},
            {"input": "nums = [4,5,6,7,0,1,2], target = 3", "output": "-1", "explanation": ""}
        ],
        "constraints": ["1 <= nums.length <= 5000", "-10^4 <= nums[i] <= 10^4", "All values of nums are unique", "nums is an ascending array that is possibly rotated"],
        "starter_code": {
            "python": "def search(nums: list[int], target: int) -> int:\n    # Your code here\n    pass",
            "javascript": "function search(nums, target) {\n    // Your code here\n}",
            "java": "public class Solution {\n    public static int search(int[] nums, int target) {\n        // Your code here\n        return -1;\n    }\n\n    public static void main(String[] args) {\n        System.out.println(search(new int[]{4,5,6,7,0,1,2}, 0));\n    }\n}"
        },
        "test_cases": [
            {"input": {"nums": [4,5,6,7,0,1,2], "target": 0}, "expected": 4},
            {"input": {"nums": [4,5,6,7,0,1,2], "target": 3}, "expected": -1},
            {"input": {"nums": [1], "target": 0}, "expected": -1},
            {"input": {"nums": [1], "target": 1}, "expected": 0},
            {"input": {"nums": [3,1], "target": 1}, "expected": 1},
            {"input": {"nums": [1,3], "target": 3}, "expected": 1},
            {"input": {"nums": [5,1,2,3,4], "target": 1}, "expected": 1},
            {"input": {"nums": [4,5,6,7,0,1,2], "target": 5}, "expected": 1},
            {"input": {"nums": [1,2,3,4,5], "target": 3}, "expected": 2}
        ],
        "tags": ["array", "binary-search"],
        "companies": ["amazon", "google", "meta", "microsoft"],
        "frequency": "high",
        "category": "blind75"
    },
    {
        "id": "find-minimum-in-rotated-sorted-array",
        "title": "Find Minimum in Rotated Sorted Array",
        "difficulty": "medium",
        "description": "Suppose an array of length `n` sorted in ascending order is rotated between `1` and `n` times. Given the sorted rotated array `nums` of unique elements, return the minimum element.\n\nYou must write an algorithm that runs in `O(log n)` time.",
        "examples": [
            {"input": "nums = [3,4,5,1,2]", "output": "1", "explanation": "The original array was [1,2,3,4,5] rotated 3 times."},
            {"input": "nums = [4,5,6,7,0,1,2]", "output": "0", "explanation": ""}
        ],
        "constraints": ["n == nums.length", "1 <= n <= 5000", "-5000 <= nums[i] <= 5000", "All integers are unique"],
        "starter_code": {
            "python": "def find_min(nums: list[int]) -> int:\n    # Your code here\n    pass",
            "javascript": "function findMin(nums) {\n    // Your code here\n}",
            "java": "public class Solution {\n    public static int findMin(int[] nums) {\n        // Your code here\n        return 0;\n    }\n\n    public static void main(String[] args) {\n        System.out.println(findMin(new int[]{3,4,5,1,2}));\n    }\n}"
        },
        "test_cases": [
            {"input": {"nums": [3,4,5,1,2]}, "expected": 1},
            {"input": {"nums": [4,5,6,7,0,1,2]}, "expected": 0},
            {"input": {"nums": [11,13,15,17]}, "expected": 11},
            {"input": {"nums": [1]}, "expected": 1},
            {"input": {"nums": [2,1]}, "expected": 1},
            {"input": {"nums": [1,2]}, "expected": 1},
            {"input": {"nums": [3,1,2]}, "expected": 1},
            {"input": {"nums": [5,6,7,8,1,2,3,4]}, "expected": 1},
            {"input": {"nums": [2,3,4,5,1]}, "expected": 1}
        ],
        "tags": ["array", "binary-search"],
        "companies": ["amazon", "google", "microsoft"],
        "frequency": "medium",
        "category": "blind75"
    },
    # --- Trees ---
    {
        "id": "same-tree",
        "title": "Same Tree",
        "difficulty": "easy",
        "description": "Given the roots of two binary trees `p` and `q`, write a function to check if they are the same or not.\n\nTwo binary trees are considered the same if they are structurally identical, and the nodes have the same value.",
        "examples": [
            {"input": "p = [1,2,3], q = [1,2,3]", "output": "true", "explanation": ""},
            {"input": "p = [1,2], q = [1,null,2]", "output": "false", "explanation": ""}
        ],
        "constraints": ["The number of nodes is in range [0, 100]", "-10^4 <= Node.val <= 10^4"],
        "starter_code": {
            "python": "def is_same_tree(p: list, q: list) -> bool:\n    # Your code here\n    pass",
            "javascript": "function isSameTree(p, q) {\n    // Your code here\n}",
            "java": "public class Solution {\n    public static boolean isSameTree(int[] p, int[] q) {\n        // Your code here\n        return false;\n    }\n\n    public static void main(String[] args) {\n        System.out.println(isSameTree(new int[]{1,2,3}, new int[]{1,2,3}));\n    }\n}"
        },
        "test_cases": [
            {"input": {"p": [1,2,3], "q": [1,2,3]}, "expected": True},
            {"input": {"p": [1,2], "q": [1,None,2]}, "expected": False},
            {"input": {"p": [1,2,1], "q": [1,1,2]}, "expected": False},
            {"input": {"p": [], "q": []}, "expected": True},
            {"input": {"p": [1], "q": [1]}, "expected": True},
            {"input": {"p": [1], "q": [2]}, "expected": False},
            {"input": {"p": [1], "q": []}, "expected": False},
            {"input": {"p": [], "q": [1]}, "expected": False}
        ],
        "tags": ["tree", "dfs", "bfs"],
        "companies": ["amazon", "google"],
        "frequency": "low",
        "category": "blind75"
    },
    {
        "id": "subtree-of-another-tree",
        "title": "Subtree of Another Tree",
        "difficulty": "easy",
        "description": "Given the roots of two binary trees `root` and `subRoot`, return `true` if there is a subtree of `root` with the same structure and node values of `subRoot` and `false` otherwise.",
        "examples": [
            {"input": "root = [3,4,5,1,2], subRoot = [4,1,2]", "output": "true", "explanation": ""},
            {"input": "root = [3,4,5,1,2,null,null,null,null,0], subRoot = [4,1,2]", "output": "false", "explanation": ""}
        ],
        "constraints": ["Number of nodes in root is in range [1, 2000]", "Number of nodes in subRoot is in range [1, 1000]"],
        "starter_code": {
            "python": "def is_subtree(root: list, subRoot: list) -> bool:\n    # Your code here\n    pass",
            "javascript": "function isSubtree(root, subRoot) {\n    // Your code here\n}",
            "java": "public class Solution {\n    public static boolean isSubtree(int[] root, int[] subRoot) {\n        // Your code here\n        return false;\n    }\n\n    public static void main(String[] args) {\n        System.out.println(isSubtree(new int[]{3,4,5,1,2}, new int[]{4,1,2}));\n    }\n}"
        },
        "test_cases": [
            {"input": {"root": [3,4,5,1,2], "subRoot": [4,1,2]}, "expected": True},
            {"input": {"root": [3,4,5,1,2,None,None,None,None,0], "subRoot": [4,1,2]}, "expected": False},
            {"input": {"root": [1], "subRoot": [1]}, "expected": True},
            {"input": {"root": [1,2], "subRoot": [1]}, "expected": False},
            {"input": {"root": [1,2,3], "subRoot": [2]}, "expected": True},
            {"input": {"root": [1,2,3], "subRoot": [3]}, "expected": True},
            {"input": {"root": [1,2,3,4,5], "subRoot": [2,4,5]}, "expected": True},
            {"input": {"root": [1,None,2], "subRoot": [2]}, "expected": True}
        ],
        "tags": ["tree", "dfs", "binary-tree"],
        "companies": ["amazon", "meta"],
        "frequency": "low",
        "category": "blind75"
    },
    {
        "id": "lowest-common-ancestor",
        "title": "Lowest Common Ancestor of BST",
        "difficulty": "medium",
        "description": "Given a binary search tree (BST), find the lowest common ancestor (LCA) node of two given nodes in the BST.\n\nThe LCA is defined as the lowest node in T that has both `p` and `q` as descendants (where a node can be a descendant of itself).",
        "examples": [
            {"input": "root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8", "output": "6", "explanation": "The LCA of nodes 2 and 8 is 6."},
            {"input": "root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 4", "output": "2", "explanation": "The LCA of nodes 2 and 4 is 2."}
        ],
        "constraints": ["Number of nodes in tree is in [2, 10^5]", "All Node.val are unique", "p != q", "p and q will exist in the BST"],
        "starter_code": {
            "python": "def lowest_common_ancestor(root: list, p: int, q: int) -> int:\n    # Your code here\n    pass",
            "javascript": "function lowestCommonAncestor(root, p, q) {\n    // Your code here\n}",
            "java": "public class Solution {\n    public static int lowestCommonAncestor(int[] root, int p, int q) {\n        // Your code here\n        return 0;\n    }\n\n    public static void main(String[] args) {\n        System.out.println(lowestCommonAncestor(new int[]{6,2,8,0,4,7,9}, 2, 8));\n    }\n}"
        },
        "test_cases": [
            {"input": {"root": [6,2,8,0,4,7,9], "p": 2, "q": 8}, "expected": 6},
            {"input": {"root": [6,2,8,0,4,7,9], "p": 2, "q": 4}, "expected": 2},
            {"input": {"root": [2,1], "p": 2, "q": 1}, "expected": 2},
            {"input": {"root": [6,2,8,0,4,7,9], "p": 0, "q": 4}, "expected": 2},
            {"input": {"root": [6,2,8,0,4,7,9], "p": 7, "q": 9}, "expected": 8},
            {"input": {"root": [6,2,8,0,4,7,9], "p": 0, "q": 9}, "expected": 6},
            {"input": {"root": [3,1,5,0,2,4,6], "p": 0, "q": 2}, "expected": 1},
            {"input": {"root": [3,1,5,0,2,4,6], "p": 4, "q": 6}, "expected": 5}
        ],
        "tags": ["tree", "dfs", "binary-search-tree"],
        "companies": ["amazon", "meta", "microsoft"],
        "frequency": "medium",
        "category": "blind75"
    },
    {
        "id": "binary-tree-level-order-traversal",
        "title": "Binary Tree Level Order Traversal",
        "difficulty": "medium",
        "description": "Given the `root` of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).",
        "examples": [
            {"input": "root = [3,9,20,null,null,15,7]", "output": "[[3],[9,20],[15,7]]", "explanation": ""},
            {"input": "root = [1]", "output": "[[1]]", "explanation": ""}
        ],
        "constraints": ["The number of nodes is in range [0, 2000]", "-1000 <= Node.val <= 1000"],
        "starter_code": {
            "python": "def level_order(root: list) -> list[list[int]]:\n    # Your code here\n    pass",
            "javascript": "function levelOrder(root) {\n    // Your code here\n}",
            "java": "import java.util.*;\n\npublic class Solution {\n    public static List<List<Integer>> levelOrder(Integer[] root) {\n        // Your code here\n        return new ArrayList<>();\n    }\n\n    public static void main(String[] args) {\n        System.out.println(levelOrder(new Integer[]{3,9,20,null,null,15,7}));\n    }\n}"
        },
        "test_cases": [
            {"input": {"root": [3,9,20,None,None,15,7]}, "expected": [[3],[9,20],[15,7]]},
            {"input": {"root": [1]}, "expected": [[1]]},
            {"input": {"root": []}, "expected": []},
            {"input": {"root": [1,2,3,4,5,6,7]}, "expected": [[1],[2,3],[4,5,6,7]]},
            {"input": {"root": [1,2,None,3]}, "expected": [[1],[2],[3]]},
            {"input": {"root": [1,None,2,None,3]}, "expected": [[1],[2],[3]]},
            {"input": {"root": [1,2,3]}, "expected": [[1],[2,3]]},
            {"input": {"root": [0]}, "expected": [[0]]}
        ],
        "tags": ["tree", "bfs"],
        "companies": ["amazon", "meta", "google"],
        "frequency": "high",
        "category": "blind75"
    },
    {
        "id": "kth-smallest-element-in-bst",
        "title": "Kth Smallest Element in a BST",
        "difficulty": "medium",
        "description": "Given the `root` of a binary search tree, and an integer `k`, return the `kth` smallest value (1-indexed) of all the values of the nodes in the tree.",
        "examples": [
            {"input": "root = [3,1,4,null,2], k = 1", "output": "1", "explanation": ""},
            {"input": "root = [5,3,6,2,4,null,null,1], k = 3", "output": "3", "explanation": ""}
        ],
        "constraints": ["Number of nodes is n", "1 <= k <= n <= 10^4", "0 <= Node.val <= 10^4"],
        "starter_code": {
            "python": "def kth_smallest(root: list, k: int) -> int:\n    # Your code here\n    pass",
            "javascript": "function kthSmallest(root, k) {\n    // Your code here\n}",
            "java": "import java.util.*;\n\npublic class Solution {\n    public static int kthSmallest(Integer[] root, int k) {\n        // Your code here\n        return 0;\n    }\n\n    public static void main(String[] args) {\n        System.out.println(kthSmallest(new Integer[]{3,1,4,null,2}, 1));\n    }\n}"
        },
        "test_cases": [
            {"input": {"root": [3,1,4,None,2], "k": 1}, "expected": 1},
            {"input": {"root": [5,3,6,2,4,None,None,1], "k": 3}, "expected": 3},
            {"input": {"root": [1], "k": 1}, "expected": 1},
            {"input": {"root": [2,1,3], "k": 2}, "expected": 2},
            {"input": {"root": [2,1,3], "k": 3}, "expected": 3},
            {"input": {"root": [5,3,7,1,4,6,8], "k": 4}, "expected": 5},
            {"input": {"root": [5,3,7,1,4,6,8], "k": 7}, "expected": 8},
            {"input": {"root": [3,1,4,None,2], "k": 2}, "expected": 2}
        ],
        "tags": ["tree", "dfs", "binary-search-tree"],
        "companies": ["amazon", "google"],
        "frequency": "medium",
        "category": "blind75"
    },
    {
        "id": "construct-binary-tree-preorder-inorder",
        "title": "Construct Binary Tree from Preorder and Inorder",
        "difficulty": "medium",
        "description": "Given two integer arrays `preorder` and `inorder` where `preorder` is the preorder traversal of a binary tree and `inorder` is the inorder traversal of the same tree, construct and return the binary tree (as a level-order array).",
        "examples": [
            {"input": "preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]", "output": "[3,9,20,null,null,15,7]", "explanation": ""}
        ],
        "constraints": ["1 <= preorder.length <= 3000", "preorder.length == inorder.length", "All values are unique"],
        "starter_code": {
            "python": "def build_tree(preorder: list[int], inorder: list[int]) -> list:\n    # Your code here\n    pass",
            "javascript": "function buildTree(preorder, inorder) {\n    // Your code here\n}",
            "java": "import java.util.*;\n\npublic class Solution {\n    public static Integer[] buildTree(int[] preorder, int[] inorder) {\n        // Your code here\n        return new Integer[]{};\n    }\n\n    public static void main(String[] args) {\n        System.out.println(Arrays.toString(buildTree(new int[]{3,9,20,15,7}, new int[]{9,3,15,20,7})));\n    }\n}"
        },
        "test_cases": [
            {"input": {"preorder": [3,9,20,15,7], "inorder": [9,3,15,20,7]}, "expected": [3,9,20,None,None,15,7]},
            {"input": {"preorder": [-1], "inorder": [-1]}, "expected": [-1]},
            {"input": {"preorder": [1,2], "inorder": [2,1]}, "expected": [1,2]},
            {"input": {"preorder": [1,2], "inorder": [1,2]}, "expected": [1,None,2]},
            {"input": {"preorder": [1,2,3], "inorder": [2,1,3]}, "expected": [1,2,3]},
            {"input": {"preorder": [1,2,4,5,3,6,7], "inorder": [4,2,5,1,6,3,7]}, "expected": [1,2,3,4,5,6,7]}
        ],
        "tags": ["tree", "divide-and-conquer", "hash-table"],
        "companies": ["amazon", "google", "microsoft"],
        "frequency": "medium",
        "category": "blind75"
    },
    # --- Heap / Priority Queue ---
    {
        "id": "find-median-from-data-stream",
        "title": "Find Median from Data Stream",
        "difficulty": "hard",
        "description": "The median is the middle value in an ordered integer list. If the size is even, the median is the average of the two middle values.\n\nImplement the `MedianFinder` class:\n- `MedianFinder()` initializes the object.\n- `void addNum(int num)` adds the integer from the data stream.\n- `double findMedian()` returns the median of all elements so far.",
        "examples": [
            {"input": "addNum(1), addNum(2), findMedian(), addNum(3), findMedian()", "output": "[1.5, 2.0]", "explanation": ""}
        ],
        "constraints": ["-10^5 <= num <= 10^5", "At most 5 * 10^4 calls will be made"],
        "starter_code": {
            "python": "import heapq\n\nclass MedianFinder:\n    def __init__(self):\n        # Your code here\n        pass\n\n    def addNum(self, num: int) -> None:\n        pass\n\n    def findMedian(self) -> float:\n        pass",
            "javascript": "class MedianFinder {\n    constructor() {\n        // Your code here\n    }\n\n    addNum(num) {\n    }\n\n    findMedian() {\n    }\n}",
            "java": "import java.util.*;\n\npublic class Solution {\n    static PriorityQueue<Integer> small = new PriorityQueue<>(Collections.reverseOrder());\n    static PriorityQueue<Integer> large = new PriorityQueue<>();\n\n    public static void addNum(int num) {\n        // Your code here\n    }\n\n    public static double findMedian() {\n        // Your code here\n        return 0.0;\n    }\n\n    public static void main(String[] args) {\n        addNum(1); addNum(2);\n        System.out.println(findMedian());\n        addNum(3);\n        System.out.println(findMedian());\n    }\n}"
        },
        "test_cases": [],
        "tags": ["heap", "design", "sorting"],
        "companies": ["amazon", "google", "meta"],
        "frequency": "high",
        "category": "blind75"
    },
    # --- Greedy ---
    {
        "id": "maximum-product-subarray",
        "title": "Maximum Product Subarray",
        "difficulty": "medium",
        "description": "Given an integer array `nums`, find a subarray that has the largest product, and return the product.\n\nThe test cases are generated so that the answer will fit in a 32-bit integer.",
        "examples": [
            {"input": "nums = [2,3,-2,4]", "output": "6", "explanation": "[2,3] has the largest product 6."},
            {"input": "nums = [-2,0,-1]", "output": "0", "explanation": "The result cannot be 2, because [-2,-1] is not a subarray."}
        ],
        "constraints": ["1 <= nums.length <= 2 * 10^4", "-10 <= nums[i] <= 10"],
        "starter_code": {
            "python": "def max_product(nums: list[int]) -> int:\n    # Your code here\n    pass",
            "javascript": "function maxProduct(nums) {\n    // Your code here\n}",
            "java": "public class Solution {\n    public static int maxProduct(int[] nums) {\n        // Your code here\n        return 0;\n    }\n\n    public static void main(String[] args) {\n        System.out.println(maxProduct(new int[]{2,3,-2,4}));\n    }\n}"
        },
        "test_cases": [
            {"input": {"nums": [2,3,-2,4]}, "expected": 6},
            {"input": {"nums": [-2,0,-1]}, "expected": 0},
            {"input": {"nums": [-2]}, "expected": -2},
            {"input": {"nums": [0]}, "expected": 0},
            {"input": {"nums": [-2,3,-4]}, "expected": 24},
            {"input": {"nums": [2,-5,-2,-4,3]}, "expected": 24},
            {"input": {"nums": [1,2,3,4]}, "expected": 24},
            {"input": {"nums": [-1,-2,-3,0]}, "expected": 6},
            {"input": {"nums": [0,2]}, "expected": 2},
            {"input": {"nums": [-4,-3,-2]}, "expected": 12}
        ],
        "tags": ["array", "dynamic-programming"],
        "companies": ["amazon", "google", "microsoft"],
        "frequency": "high",
        "category": "blind75"
    },
    {
        "id": "jump-game",
        "title": "Jump Game",
        "difficulty": "medium",
        "description": "You are given an integer array `nums`. You are initially positioned at the array's first index, and each element represents your maximum jump length at that position.\n\nReturn `true` if you can reach the last index, or `false` otherwise.",
        "examples": [
            {"input": "nums = [2,3,1,1,4]", "output": "true", "explanation": "Jump 1 step from index 0 to 1, then 3 steps to the last index."},
            {"input": "nums = [3,2,1,0,4]", "output": "false", "explanation": "You will always arrive at index 3, whose jump length is 0."}
        ],
        "constraints": ["1 <= nums.length <= 10^4", "0 <= nums[i] <= 10^5"],
        "starter_code": {
            "python": "def can_jump(nums: list[int]) -> bool:\n    # Your code here\n    pass",
            "javascript": "function canJump(nums) {\n    // Your code here\n}",
            "java": "public class Solution {\n    public static boolean canJump(int[] nums) {\n        // Your code here\n        return false;\n    }\n\n    public static void main(String[] args) {\n        System.out.println(canJump(new int[]{2,3,1,1,4}));\n    }\n}"
        },
        "test_cases": [
            {"input": {"nums": [2,3,1,1,4]}, "expected": True},
            {"input": {"nums": [3,2,1,0,4]}, "expected": False},
            {"input": {"nums": [0]}, "expected": True},
            {"input": {"nums": [1,0]}, "expected": True},
            {"input": {"nums": [0,1]}, "expected": False},
            {"input": {"nums": [2,0,0]}, "expected": True},
            {"input": {"nums": [1,1,1,1,1]}, "expected": True},
            {"input": {"nums": [5,0,0,0,0,0]}, "expected": True},
            {"input": {"nums": [1,2,3]}, "expected": True},
            {"input": {"nums": [1,0,1,0]}, "expected": False}
        ],
        "tags": ["array", "greedy", "dynamic-programming"],
        "companies": ["amazon", "google", "meta"],
        "frequency": "high",
        "category": "blind75"
    },
    # --- Intervals ---
    {
        "id": "non-overlapping-intervals",
        "title": "Non-overlapping Intervals",
        "difficulty": "medium",
        "description": "Given an array of intervals `intervals` where `intervals[i] = [start_i, end_i]`, return the minimum number of intervals you need to remove to make the rest of the intervals non-overlapping.",
        "examples": [
            {"input": "intervals = [[1,2],[2,3],[3,4],[1,3]]", "output": "1", "explanation": "[1,3] can be removed and the rest are non-overlapping."},
            {"input": "intervals = [[1,2],[1,2],[1,2]]", "output": "2", "explanation": "You need to remove two [1,2] to make the rest non-overlapping."}
        ],
        "constraints": ["1 <= intervals.length <= 10^5", "intervals[i].length == 2"],
        "starter_code": {
            "python": "def erase_overlap_intervals(intervals: list[list[int]]) -> int:\n    # Your code here\n    pass",
            "javascript": "function eraseOverlapIntervals(intervals) {\n    // Your code here\n}",
            "java": "import java.util.*;\n\npublic class Solution {\n    public static int eraseOverlapIntervals(int[][] intervals) {\n        // Your code here\n        return 0;\n    }\n\n    public static void main(String[] args) {\n        System.out.println(eraseOverlapIntervals(new int[][]{{1,2},{2,3},{3,4},{1,3}}));\n    }\n}"
        },
        "test_cases": [
            {"input": {"intervals": [[1,2],[2,3],[3,4],[1,3]]}, "expected": 1},
            {"input": {"intervals": [[1,2],[1,2],[1,2]]}, "expected": 2},
            {"input": {"intervals": [[1,2],[2,3]]}, "expected": 0},
            {"input": {"intervals": [[1,100],[11,22],[1,11],[2,12]]}, "expected": 2},
            {"input": {"intervals": [[0,2],[1,3],[2,4],[3,5],[4,6]]}, "expected": 2},
            {"input": {"intervals": [[1,2]]}, "expected": 0},
            {"input": {"intervals": [[-1,0],[0,1]]}, "expected": 0},
            {"input": {"intervals": [[1,3],[2,4],[3,5]]}, "expected": 1}
        ],
        "tags": ["array", "greedy", "sorting"],
        "companies": ["amazon", "google"],
        "frequency": "medium",
        "category": "blind75"
    },
    {
        "id": "insert-interval",
        "title": "Insert Interval",
        "difficulty": "medium",
        "description": "You are given an array of non-overlapping intervals `intervals` where `intervals[i] = [start_i, end_i]`, sorted in ascending order by `start_i`. You are also given an interval `newInterval = [start, end]`.\n\nInsert `newInterval` into `intervals` such that `intervals` is still sorted and non-overlapping (merge if necessary). Return `intervals` after the insertion.",
        "examples": [
            {"input": "intervals = [[1,3],[6,9]], newInterval = [2,5]", "output": "[[1,5],[6,9]]", "explanation": ""},
            {"input": "intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]", "output": "[[1,2],[3,10],[12,16]]", "explanation": "The new interval [4,8] overlaps with [3,5],[6,7],[8,10]."}
        ],
        "constraints": ["0 <= intervals.length <= 10^4", "intervals[i].length == 2", "intervals is sorted by start_i"],
        "starter_code": {
            "python": "def insert(intervals: list[list[int]], newInterval: list[int]) -> list[list[int]]:\n    # Your code here\n    pass",
            "javascript": "function insert(intervals, newInterval) {\n    // Your code here\n}",
            "java": "import java.util.*;\n\npublic class Solution {\n    public static int[][] insert(int[][] intervals, int[] newInterval) {\n        // Your code here\n        return new int[][]{};\n    }\n\n    public static void main(String[] args) {\n        int[][] result = insert(new int[][]{{1,3},{6,9}}, new int[]{2,5});\n        for (int[] r : result) System.out.println(Arrays.toString(r));\n    }\n}"
        },
        "test_cases": [
            {"input": {"intervals": [[1,3],[6,9]], "newInterval": [2,5]}, "expected": [[1,5],[6,9]]},
            {"input": {"intervals": [[1,2],[3,5],[6,7],[8,10],[12,16]], "newInterval": [4,8]}, "expected": [[1,2],[3,10],[12,16]]},
            {"input": {"intervals": [], "newInterval": [5,7]}, "expected": [[5,7]]},
            {"input": {"intervals": [[1,5]], "newInterval": [2,3]}, "expected": [[1,5]]},
            {"input": {"intervals": [[1,5]], "newInterval": [6,8]}, "expected": [[1,5],[6,8]]},
            {"input": {"intervals": [[1,5]], "newInterval": [0,0]}, "expected": [[0,0],[1,5]]},
            {"input": {"intervals": [[1,5]], "newInterval": [0,6]}, "expected": [[0,6]]},
            {"input": {"intervals": [[3,5],[12,15]], "newInterval": [6,6]}, "expected": [[3,5],[6,6],[12,15]]}
        ],
        "tags": ["array", "intervals"],
        "companies": ["amazon", "google", "meta"],
        "frequency": "high",
        "category": "blind75"
    },
    # --- DP ---
    {
        "id": "unique-paths",
        "title": "Unique Paths",
        "difficulty": "medium",
        "description": "There is a robot on an `m x n` grid. The robot is initially located at the top-left corner. The robot tries to move to the bottom-right corner. The robot can only move either down or right at any point in time.\n\nGiven the two integers `m` and `n`, return the number of possible unique paths.",
        "examples": [
            {"input": "m = 3, n = 7", "output": "28", "explanation": ""},
            {"input": "m = 3, n = 2", "output": "3", "explanation": "From top-left to bottom-right, there are 3 paths."}
        ],
        "constraints": ["1 <= m, n <= 100"],
        "starter_code": {
            "python": "def unique_paths(m: int, n: int) -> int:\n    # Your code here\n    pass",
            "javascript": "function uniquePaths(m, n) {\n    // Your code here\n}",
            "java": "public class Solution {\n    public static int uniquePaths(int m, int n) {\n        // Your code here\n        return 0;\n    }\n\n    public static void main(String[] args) {\n        System.out.println(uniquePaths(3, 7));\n    }\n}"
        },
        "test_cases": [
            {"input": {"m": 3, "n": 7}, "expected": 28},
            {"input": {"m": 3, "n": 2}, "expected": 3},
            {"input": {"m": 1, "n": 1}, "expected": 1},
            {"input": {"m": 1, "n": 5}, "expected": 1},
            {"input": {"m": 5, "n": 1}, "expected": 1},
            {"input": {"m": 2, "n": 2}, "expected": 2},
            {"input": {"m": 3, "n": 3}, "expected": 6},
            {"input": {"m": 4, "n": 4}, "expected": 20},
            {"input": {"m": 7, "n": 3}, "expected": 28},
            {"input": {"m": 10, "n": 10}, "expected": 48620}
        ],
        "tags": ["dynamic-programming", "math", "combinatorics"],
        "companies": ["amazon", "google"],
        "frequency": "medium",
        "category": "blind75"
    },
    {
        "id": "decode-ways",
        "title": "Decode Ways",
        "difficulty": "medium",
        "description": "A message containing letters from `A-Z` can be encoded by mapping `'A' -> \"1\"`, `'B' -> \"2\"`, ..., `'Z' -> \"26\"`.\n\nGiven a string `s` containing only digits, return the number of ways to decode it. The answer is guaranteed to fit in a 32-bit integer.",
        "examples": [
            {"input": 's = "12"', "output": "2", "explanation": "'12' could be decoded as 'AB' (1 2) or 'L' (12)."},
            {"input": 's = "226"', "output": "3", "explanation": "'226' could be decoded as 'BZ' (2 26), 'VF' (22 6), or 'BBF' (2 2 6)."}
        ],
        "constraints": ["1 <= s.length <= 100", "s contains only digits and may contain leading zeros"],
        "starter_code": {
            "python": "def num_decodings(s: str) -> int:\n    # Your code here\n    pass",
            "javascript": "function numDecodings(s) {\n    // Your code here\n}",
            "java": "public class Solution {\n    public static int numDecodings(String s) {\n        // Your code here\n        return 0;\n    }\n\n    public static void main(String[] args) {\n        System.out.println(numDecodings(\"226\"));\n    }\n}"
        },
        "test_cases": [
            {"input": {"s": "12"}, "expected": 2},
            {"input": {"s": "226"}, "expected": 3},
            {"input": {"s": "06"}, "expected": 0},
            {"input": {"s": "0"}, "expected": 0},
            {"input": {"s": "1"}, "expected": 1},
            {"input": {"s": "10"}, "expected": 1},
            {"input": {"s": "27"}, "expected": 1},
            {"input": {"s": "11106"}, "expected": 2},
            {"input": {"s": "111"}, "expected": 3},
            {"input": {"s": "2611055971"}, "expected": 4}
        ],
        "tags": ["string", "dynamic-programming"],
        "companies": ["amazon", "google", "meta"],
        "frequency": "medium",
        "category": "blind75"
    },
    {
        "id": "house-robber",
        "title": "House Robber",
        "difficulty": "medium",
        "description": "You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed. Adjacent houses have security systems connected — if two adjacent houses were broken into on the same night, it will alert the police.\n\nGiven an integer array `nums` representing the amount at each house, return the maximum amount you can rob without alerting the police.",
        "examples": [
            {"input": "nums = [1,2,3,1]", "output": "4", "explanation": "Rob house 1 (money = 1) and then rob house 3 (money = 3). Total = 4."},
            {"input": "nums = [2,7,9,3,1]", "output": "12", "explanation": "Rob house 1, 3, 5. Total = 2 + 9 + 1 = 12."}
        ],
        "constraints": ["1 <= nums.length <= 100", "0 <= nums[i] <= 400"],
        "starter_code": {
            "python": "def rob(nums: list[int]) -> int:\n    # Your code here\n    pass",
            "javascript": "function rob(nums) {\n    // Your code here\n}",
            "java": "public class Solution {\n    public static int rob(int[] nums) {\n        // Your code here\n        return 0;\n    }\n\n    public static void main(String[] args) {\n        System.out.println(rob(new int[]{2,7,9,3,1}));\n    }\n}"
        },
        "test_cases": [
            {"input": {"nums": [1,2,3,1]}, "expected": 4},
            {"input": {"nums": [2,7,9,3,1]}, "expected": 12},
            {"input": {"nums": [0]}, "expected": 0},
            {"input": {"nums": [1]}, "expected": 1},
            {"input": {"nums": [1,2]}, "expected": 2},
            {"input": {"nums": [2,1]}, "expected": 2},
            {"input": {"nums": [1,2,3]}, "expected": 4},
            {"input": {"nums": [100,1,1,100]}, "expected": 200},
            {"input": {"nums": [1,3,1,3,100]}, "expected": 103},
            {"input": {"nums": [2,1,1,2]}, "expected": 4}
        ],
        "tags": ["array", "dynamic-programming"],
        "companies": ["amazon", "google"],
        "frequency": "high",
        "category": "blind75"
    },
    {
        "id": "house-robber-ii",
        "title": "House Robber II",
        "difficulty": "medium",
        "description": "You are a robber planning to rob houses arranged in a circle. That means the first house is the neighbor of the last one. Adjacent houses have security systems — you cannot rob two adjacent houses.\n\nGiven an integer array `nums` representing money at each house, return the maximum amount you can rob.",
        "examples": [
            {"input": "nums = [2,3,2]", "output": "3", "explanation": "You cannot rob house 1 (money = 2) and house 3 (money = 2), because they are adjacent."},
            {"input": "nums = [1,2,3,1]", "output": "4", "explanation": "Rob house 1 (1) and house 3 (3). Total = 4."}
        ],
        "constraints": ["1 <= nums.length <= 100", "0 <= nums[i] <= 1000"],
        "starter_code": {
            "python": "def rob(nums: list[int]) -> int:\n    # Your code here\n    pass",
            "javascript": "function rob(nums) {\n    // Your code here\n}",
            "java": "public class Solution {\n    public static int rob(int[] nums) {\n        // Your code here\n        return 0;\n    }\n\n    public static void main(String[] args) {\n        System.out.println(rob(new int[]{2,3,2}));\n    }\n}"
        },
        "test_cases": [
            {"input": {"nums": [2,3,2]}, "expected": 3},
            {"input": {"nums": [1,2,3,1]}, "expected": 4},
            {"input": {"nums": [1,2,3]}, "expected": 3},
            {"input": {"nums": [1]}, "expected": 1},
            {"input": {"nums": [1,2]}, "expected": 2},
            {"input": {"nums": [0,0,0]}, "expected": 0},
            {"input": {"nums": [200,3,140,20,10]}, "expected": 340},
            {"input": {"nums": [1,3,1,3,100]}, "expected": 103},
            {"input": {"nums": [4,1,2,7,5,3,1]}, "expected": 14}
        ],
        "tags": ["array", "dynamic-programming"],
        "companies": ["amazon", "google"],
        "frequency": "medium",
        "category": "blind75"
    },
    {
        "id": "longest-palindromic-substring",
        "title": "Longest Palindromic Substring",
        "difficulty": "medium",
        "description": "Given a string `s`, return the longest palindromic substring in `s`.",
        "examples": [
            {"input": 's = "babad"', "output": '"bab"', "explanation": "'aba' is also a valid answer."},
            {"input": 's = "cbbd"', "output": '"bb"', "explanation": ""}
        ],
        "constraints": ["1 <= s.length <= 1000", "s consist of only digits and English letters"],
        "starter_code": {
            "python": "def longest_palindrome(s: str) -> str:\n    # Your code here\n    pass",
            "javascript": "function longestPalindrome(s) {\n    // Your code here\n}",
            "java": "public class Solution {\n    public static String longestPalindrome(String s) {\n        // Your code here\n        return \"\";\n    }\n\n    public static void main(String[] args) {\n        System.out.println(longestPalindrome(\"babad\"));\n    }\n}"
        },
        "test_cases": [
            {"input": {"s": "babad"}, "expected": "bab"},
            {"input": {"s": "cbbd"}, "expected": "bb"},
            {"input": {"s": "a"}, "expected": "a"},
            {"input": {"s": "ac"}, "expected": "a"},
            {"input": {"s": "racecar"}, "expected": "racecar"},
            {"input": {"s": "aacabdkacaa"}, "expected": "aca"},
            {"input": {"s": "aaaa"}, "expected": "aaaa"},
            {"input": {"s": "abcba"}, "expected": "abcba"},
            {"input": {"s": "xabaay"}, "expected": "abaay"}
        ],
        "tags": ["string", "dynamic-programming", "two-pointers"],
        "companies": ["amazon", "google", "meta", "microsoft"],
        "frequency": "high",
        "category": "blind75"
    },
    {
        "id": "palindromic-substrings",
        "title": "Palindromic Substrings",
        "difficulty": "medium",
        "description": "Given a string `s`, return the number of palindromic substrings in it.\n\nA string is a palindrome when it reads the same backward as forward. A substring is a contiguous sequence of characters within the string.",
        "examples": [
            {"input": 's = "abc"', "output": "3", "explanation": "Three palindromic strings: 'a', 'b', 'c'."},
            {"input": 's = "aaa"', "output": "6", "explanation": "Six palindromic strings: 'a', 'a', 'a', 'aa', 'aa', 'aaa'."}
        ],
        "constraints": ["1 <= s.length <= 1000", "s consists of lowercase English letters"],
        "starter_code": {
            "python": "def count_substrings(s: str) -> int:\n    # Your code here\n    pass",
            "javascript": "function countSubstrings(s) {\n    // Your code here\n}",
            "java": "public class Solution {\n    public static int countSubstrings(String s) {\n        // Your code here\n        return 0;\n    }\n\n    public static void main(String[] args) {\n        System.out.println(countSubstrings(\"aaa\"));\n    }\n}"
        },
        "test_cases": [
            {"input": {"s": "abc"}, "expected": 3},
            {"input": {"s": "aaa"}, "expected": 6},
            {"input": {"s": "a"}, "expected": 1},
            {"input": {"s": "ab"}, "expected": 2},
            {"input": {"s": "aa"}, "expected": 3},
            {"input": {"s": "aba"}, "expected": 4},
            {"input": {"s": "abba"}, "expected": 6},
            {"input": {"s": "abcba"}, "expected": 7},
            {"input": {"s": "racecar"}, "expected": 10}
        ],
        "tags": ["string", "dynamic-programming", "two-pointers"],
        "companies": ["amazon", "meta"],
        "frequency": "medium",
        "category": "blind75"
    },
    # --- Bit Manipulation ---
    {
        "id": "number-of-1-bits",
        "title": "Number of 1 Bits",
        "difficulty": "easy",
        "description": "Write a function that takes the binary representation of a positive integer and returns the number of set bits it has (also known as the Hamming weight).",
        "examples": [
            {"input": "n = 11", "output": "3", "explanation": "The input binary string 1011 has three set bits."},
            {"input": "n = 128", "output": "1", "explanation": "The input binary string 10000000 has one set bit."}
        ],
        "constraints": ["1 <= n <= 2^31 - 1"],
        "starter_code": {
            "python": "def hamming_weight(n: int) -> int:\n    # Your code here\n    pass",
            "javascript": "function hammingWeight(n) {\n    // Your code here\n}",
            "java": "public class Solution {\n    public static int hammingWeight(int n) {\n        // Your code here\n        return 0;\n    }\n\n    public static void main(String[] args) {\n        System.out.println(hammingWeight(11));\n        System.out.println(hammingWeight(128));\n    }\n}"
        },
        "test_cases": [
            {"input": {"n": 11}, "expected": 3},
            {"input": {"n": 128}, "expected": 1},
            {"input": {"n": 1}, "expected": 1},
            {"input": {"n": 0}, "expected": 0},
            {"input": {"n": 255}, "expected": 8},
            {"input": {"n": 7}, "expected": 3},
            {"input": {"n": 1023}, "expected": 10},
            {"input": {"n": 16}, "expected": 1},
            {"input": {"n": 31}, "expected": 5}
        ],
        "tags": ["bit-manipulation"],
        "companies": ["amazon", "google"],
        "frequency": "low",
        "category": "blind75"
    },
    {
        "id": "counting-bits",
        "title": "Counting Bits",
        "difficulty": "easy",
        "description": "Given an integer `n`, return an array `ans` of length `n + 1` such that for each `i` (`0 <= i <= n`), `ans[i]` is the number of `1`'s in the binary representation of `i`.",
        "examples": [
            {"input": "n = 2", "output": "[0,1,1]", "explanation": "0 --> 0, 1 --> 1, 2 --> 10"},
            {"input": "n = 5", "output": "[0,1,1,2,1,2]", "explanation": ""}
        ],
        "constraints": ["0 <= n <= 10^5"],
        "starter_code": {
            "python": "def count_bits(n: int) -> list[int]:\n    # Your code here\n    pass",
            "javascript": "function countBits(n) {\n    // Your code here\n}",
            "java": "import java.util.*;\n\npublic class Solution {\n    public static int[] countBits(int n) {\n        // Your code here\n        return new int[]{};\n    }\n\n    public static void main(String[] args) {\n        System.out.println(Arrays.toString(countBits(5)));\n    }\n}"
        },
        "test_cases": [
            {"input": {"n": 2}, "expected": [0,1,1]},
            {"input": {"n": 5}, "expected": [0,1,1,2,1,2]},
            {"input": {"n": 0}, "expected": [0]},
            {"input": {"n": 1}, "expected": [0,1]},
            {"input": {"n": 8}, "expected": [0,1,1,2,1,2,2,3,1]},
            {"input": {"n": 3}, "expected": [0,1,1,2]},
            {"input": {"n": 7}, "expected": [0,1,1,2,1,2,2,3]},
            {"input": {"n": 10}, "expected": [0,1,1,2,1,2,2,3,1,2,2]}
        ],
        "tags": ["bit-manipulation", "dynamic-programming"],
        "companies": ["amazon", "google"],
        "frequency": "low",
        "category": "blind75"
    },
    {
        "id": "reverse-bits",
        "title": "Reverse Bits",
        "difficulty": "easy",
        "description": "Reverse bits of a given 32 bits unsigned integer.",
        "examples": [
            {"input": "n = 43261596", "output": "964176192", "explanation": "Input: 00000010100101000001111010011100, Output: 00111001011110000010100101000000"},
            {"input": "n = 4294967293", "output": "3221225471", "explanation": ""}
        ],
        "constraints": ["The input must be a binary string of length 32"],
        "starter_code": {
            "python": "def reverse_bits(n: int) -> int:\n    # Your code here\n    pass",
            "javascript": "function reverseBits(n) {\n    // Your code here\n}",
            "java": "public class Solution {\n    public static int reverseBits(int n) {\n        // Your code here\n        return 0;\n    }\n\n    public static void main(String[] args) {\n        System.out.println(reverseBits(43261596));\n    }\n}"
        },
        "test_cases": [
            {"input": {"n": 43261596}, "expected": 964176192},
            {"input": {"n": 4294967293}, "expected": 3221225471},
            {"input": {"n": 0}, "expected": 0},
            {"input": {"n": 1}, "expected": 2147483648},
            {"input": {"n": 2}, "expected": 1073741824},
            {"input": {"n": 4294967295}, "expected": 4294967295},
            {"input": {"n": 2147483648}, "expected": 1}
        ],
        "tags": ["bit-manipulation"],
        "companies": ["amazon", "google"],
        "frequency": "low",
        "category": "blind75"
    },
    {
        "id": "missing-number",
        "title": "Missing Number",
        "difficulty": "easy",
        "description": "Given an array `nums` containing `n` distinct numbers in the range `[0, n]`, return the only number in the range that is missing from the array.",
        "examples": [
            {"input": "nums = [3,0,1]", "output": "2", "explanation": "n = 3 since there are 3 numbers, so all numbers are in range [0,3]. 2 is missing."},
            {"input": "nums = [0,1]", "output": "2", "explanation": "n = 2, 2 is missing."}
        ],
        "constraints": ["n == nums.length", "1 <= n <= 10^4", "0 <= nums[i] <= n", "All numbers are unique"],
        "starter_code": {
            "python": "def missing_number(nums: list[int]) -> int:\n    # Your code here\n    pass",
            "javascript": "function missingNumber(nums) {\n    // Your code here\n}",
            "java": "public class Solution {\n    public static int missingNumber(int[] nums) {\n        // Your code here\n        return 0;\n    }\n\n    public static void main(String[] args) {\n        System.out.println(missingNumber(new int[]{3,0,1}));\n    }\n}"
        },
        "test_cases": [
            {"input": {"nums": [3,0,1]}, "expected": 2},
            {"input": {"nums": [0,1]}, "expected": 2},
            {"input": {"nums": [9,6,4,2,3,5,7,0,1]}, "expected": 8},
            {"input": {"nums": [0]}, "expected": 1},
            {"input": {"nums": [1]}, "expected": 0},
            {"input": {"nums": [0,1,2,3,4,5,6,7,9]}, "expected": 8},
            {"input": {"nums": [1,2,3]}, "expected": 0},
            {"input": {"nums": [0,2,3]}, "expected": 1},
            {"input": {"nums": [0,1,3]}, "expected": 2}
        ],
        "tags": ["array", "bit-manipulation", "math", "sorting"],
        "companies": ["amazon", "microsoft"],
        "frequency": "low",
        "category": "blind75"
    },
    {
        "id": "sum-of-two-integers",
        "title": "Sum of Two Integers",
        "difficulty": "medium",
        "description": "Given two integers `a` and `b`, return the sum of the two integers without using the operators `+` and `-`.",
        "examples": [
            {"input": "a = 1, b = 2", "output": "3", "explanation": ""},
            {"input": "a = 2, b = 3", "output": "5", "explanation": ""}
        ],
        "constraints": ["-1000 <= a, b <= 1000"],
        "starter_code": {
            "python": "def get_sum(a: int, b: int) -> int:\n    # Your code here\n    pass",
            "javascript": "function getSum(a, b) {\n    // Your code here\n}",
            "java": "public class Solution {\n    public static int getSum(int a, int b) {\n        // Your code here\n        return 0;\n    }\n\n    public static void main(String[] args) {\n        System.out.println(getSum(1, 2));\n    }\n}"
        },
        "test_cases": [
            {"input": {"a": 1, "b": 2}, "expected": 3},
            {"input": {"a": 2, "b": 3}, "expected": 5},
            {"input": {"a": 0, "b": 0}, "expected": 0},
            {"input": {"a": -1, "b": 1}, "expected": 0},
            {"input": {"a": -1, "b": -1}, "expected": -2},
            {"input": {"a": 100, "b": 200}, "expected": 300},
            {"input": {"a": -5, "b": 3}, "expected": -2},
            {"input": {"a": 10, "b": -7}, "expected": 3}
        ],
        "tags": ["bit-manipulation", "math"],
        "companies": ["amazon", "google"],
        "frequency": "low",
        "category": "blind75"
    },
    # --- Graph ---
    {
        "id": "clone-graph",
        "title": "Clone Graph",
        "difficulty": "medium",
        "description": "Given a reference of a node in a connected undirected graph, return a deep copy (clone) of the graph.\n\nEach node contains a value (`int`) and a list of its neighbors (`List[Node]`). The graph is represented as an adjacency list.",
        "examples": [
            {"input": "adjList = [[2,4],[1,3],[2,4],[1,3]]", "output": "[[2,4],[1,3],[2,4],[1,3]]", "explanation": "There are 4 nodes in the graph."}
        ],
        "constraints": ["Number of nodes is in range [0, 100]", "1 <= Node.val <= 100", "Node.val is unique", "No self-loops or repeated edges"],
        "starter_code": {
            "python": "def clone_graph(adjList: list[list[int]]) -> list[list[int]]:\n    # Your code here — return adjacency list of cloned graph\n    pass",
            "javascript": "function cloneGraph(adjList) {\n    // Your code here\n}",
            "java": "import java.util.*;\n\npublic class Solution {\n    public static List<List<Integer>> cloneGraph(List<List<Integer>> adjList) {\n        // Your code here\n        return new ArrayList<>();\n    }\n\n    public static void main(String[] args) {\n        List<List<Integer>> adj = Arrays.asList(\n            Arrays.asList(2,4), Arrays.asList(1,3), Arrays.asList(2,4), Arrays.asList(1,3));\n        System.out.println(cloneGraph(adj));\n    }\n}"
        },
        "test_cases": [
            {"input": {"adjList": [[2,4],[1,3],[2,4],[1,3]]}, "expected": [[2,4],[1,3],[2,4],[1,3]]},
            {"input": {"adjList": [[]]}, "expected": [[]]},
            {"input": {"adjList": []}, "expected": []},
            {"input": {"adjList": [[2],[1]]}, "expected": [[2],[1]]},
            {"input": {"adjList": [[2,3],[1,3],[1,2]]}, "expected": [[2,3],[1,3],[1,2]]}
        ],
        "tags": ["graph", "dfs", "bfs", "hash-table"],
        "companies": ["amazon", "google", "meta"],
        "frequency": "medium",
        "category": "blind75"
    },
    {
        "id": "pacific-atlantic-water-flow",
        "title": "Pacific Atlantic Water Flow",
        "difficulty": "medium",
        "description": "There is an `m x n` rectangular island that borders both the Pacific Ocean and Atlantic Ocean. The Pacific Ocean touches the island's left and top edges, and the Atlantic Ocean touches the island's right and bottom edges.\n\nWater can flow from a cell to another adjacent cell if the adjacent cell's height is less than or equal to the current cell's height.\n\nReturn a 2D list of grid coordinates where water can flow to both the Pacific and Atlantic oceans.",
        "examples": [
            {"input": "heights = [[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]", "output": "[[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]", "explanation": ""}
        ],
        "constraints": ["m == heights.length", "n == heights[i].length", "1 <= m, n <= 200", "0 <= heights[i][j] <= 10^5"],
        "starter_code": {
            "python": "def pacific_atlantic(heights: list[list[int]]) -> list[list[int]]:\n    # Your code here\n    pass",
            "javascript": "function pacificAtlantic(heights) {\n    // Your code here\n}",
            "java": "import java.util.*;\n\npublic class Solution {\n    public static List<List<Integer>> pacificAtlantic(int[][] heights) {\n        // Your code here\n        return new ArrayList<>();\n    }\n\n    public static void main(String[] args) {\n        int[][] h = {{1,2,2,3,5},{3,2,3,4,4},{2,4,5,3,1},{6,7,1,4,5},{5,1,1,2,4}};\n        System.out.println(pacificAtlantic(h));\n    }\n}"
        },
        "test_cases": [
            {"input": {"heights": [[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]}, "expected": [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]},
            {"input": {"heights": [[1]]}, "expected": [[0,0]]},
            {"input": {"heights": [[1,1],[1,1]]}, "expected": [[0,0],[0,1],[1,0],[1,1]]},
            {"input": {"heights": [[1,2],[3,4]]}, "expected": [[0,1],[1,0],[1,1]]},
            {"input": {"heights": [[10,10,10],[10,1,10],[10,10,10]]}, "expected": [[0,0],[0,1],[0,2],[1,0],[1,2],[2,0],[2,1],[2,2]]}
        ],
        "tags": ["graph", "dfs", "bfs", "matrix"],
        "companies": ["amazon", "google"],
        "frequency": "medium",
        "category": "blind75"
    },
    {
        "id": "graph-valid-tree",
        "title": "Graph Valid Tree",
        "difficulty": "medium",
        "description": "Given `n` nodes labeled from `0` to `n-1` and a list of undirected `edges`, write a function to check whether these edges make up a valid tree.\n\nA valid tree has exactly `n-1` edges, is connected, and has no cycles.",
        "examples": [
            {"input": "n = 5, edges = [[0,1],[0,2],[0,3],[1,4]]", "output": "true", "explanation": ""},
            {"input": "n = 5, edges = [[0,1],[1,2],[2,3],[1,3],[1,4]]", "output": "false", "explanation": ""}
        ],
        "constraints": ["1 <= n <= 2000", "0 <= edges.length <= 5000", "edges[i].length == 2"],
        "starter_code": {
            "python": "def valid_tree(n: int, edges: list[list[int]]) -> bool:\n    # Your code here\n    pass",
            "javascript": "function validTree(n, edges) {\n    // Your code here\n}",
            "java": "import java.util.*;\n\npublic class Solution {\n    public static boolean validTree(int n, int[][] edges) {\n        // Your code here\n        return false;\n    }\n\n    public static void main(String[] args) {\n        System.out.println(validTree(5, new int[][]{{0,1},{0,2},{0,3},{1,4}}));\n    }\n}"
        },
        "test_cases": [
            {"input": {"n": 5, "edges": [[0,1],[0,2],[0,3],[1,4]]}, "expected": True},
            {"input": {"n": 5, "edges": [[0,1],[1,2],[2,3],[1,3],[1,4]]}, "expected": False},
            {"input": {"n": 1, "edges": []}, "expected": True},
            {"input": {"n": 2, "edges": [[0,1]]}, "expected": True},
            {"input": {"n": 2, "edges": []}, "expected": False},
            {"input": {"n": 4, "edges": [[0,1],[2,3]]}, "expected": False},
            {"input": {"n": 3, "edges": [[0,1],[1,2]]}, "expected": True},
            {"input": {"n": 3, "edges": [[0,1],[0,2],[1,2]]}, "expected": False}
        ],
        "tags": ["graph", "dfs", "bfs", "union-find"],
        "companies": ["amazon", "google", "meta"],
        "frequency": "medium",
        "category": "blind75"
    },
    {
        "id": "number-of-connected-components",
        "title": "Number of Connected Components",
        "difficulty": "medium",
        "description": "You have a graph of `n` nodes. You are given an integer `n` and an array `edges` where `edges[i] = [a_i, b_i]` indicates that there is an edge between `a_i` and `b_i` in the graph.\n\nReturn the number of connected components in the graph.",
        "examples": [
            {"input": "n = 5, edges = [[0,1],[1,2],[3,4]]", "output": "2", "explanation": ""},
            {"input": "n = 5, edges = [[0,1],[1,2],[2,3],[3,4]]", "output": "1", "explanation": ""}
        ],
        "constraints": ["1 <= n <= 2000", "1 <= edges.length <= 5000"],
        "starter_code": {
            "python": "def count_components(n: int, edges: list[list[int]]) -> int:\n    # Your code here\n    pass",
            "javascript": "function countComponents(n, edges) {\n    // Your code here\n}",
            "java": "import java.util.*;\n\npublic class Solution {\n    public static int countComponents(int n, int[][] edges) {\n        // Your code here\n        return 0;\n    }\n\n    public static void main(String[] args) {\n        System.out.println(countComponents(5, new int[][]{{0,1},{1,2},{3,4}}));\n    }\n}"
        },
        "test_cases": [
            {"input": {"n": 5, "edges": [[0,1],[1,2],[3,4]]}, "expected": 2},
            {"input": {"n": 5, "edges": [[0,1],[1,2],[2,3],[3,4]]}, "expected": 1},
            {"input": {"n": 1, "edges": []}, "expected": 1},
            {"input": {"n": 4, "edges": []}, "expected": 4},
            {"input": {"n": 3, "edges": [[0,1]]}, "expected": 2},
            {"input": {"n": 6, "edges": [[0,1],[2,3],[4,5]]}, "expected": 3},
            {"input": {"n": 4, "edges": [[0,1],[0,2],[0,3]]}, "expected": 1},
            {"input": {"n": 2, "edges": [[0,1]]}, "expected": 1}
        ],
        "tags": ["graph", "dfs", "bfs", "union-find"],
        "companies": ["amazon", "google"],
        "frequency": "medium",
        "category": "blind75"
    },
    # --- Remaining DP ---
    {
        "id": "longest-common-subsequence",
        "title": "Longest Common Subsequence",
        "difficulty": "medium",
        "description": "Given two strings `text1` and `text2`, return the length of their longest common subsequence. If there is no common subsequence, return `0`.\n\nA subsequence is a sequence that can be derived from another sequence by deleting some or no elements without changing the order of the remaining elements.",
        "examples": [
            {"input": 'text1 = "abcde", text2 = "ace"', "output": "3", "explanation": "The longest common subsequence is 'ace' and its length is 3."},
            {"input": 'text1 = "abc", text2 = "def"', "output": "0", "explanation": "There is no common subsequence."}
        ],
        "constraints": ["1 <= text1.length, text2.length <= 1000", "text1 and text2 consist of only lowercase English characters"],
        "starter_code": {
            "python": "def longest_common_subsequence(text1: str, text2: str) -> int:\n    # Your code here\n    pass",
            "javascript": "function longestCommonSubsequence(text1, text2) {\n    // Your code here\n}",
            "java": "public class Solution {\n    public static int longestCommonSubsequence(String text1, String text2) {\n        // Your code here\n        return 0;\n    }\n\n    public static void main(String[] args) {\n        System.out.println(longestCommonSubsequence(\"abcde\", \"ace\"));\n    }\n}"
        },
        "test_cases": [
            {"input": {"text1": "abcde", "text2": "ace"}, "expected": 3},
            {"input": {"text1": "abc", "text2": "abc"}, "expected": 3},
            {"input": {"text1": "abc", "text2": "def"}, "expected": 0},
            {"input": {"text1": "a", "text2": "a"}, "expected": 1},
            {"input": {"text1": "a", "text2": "b"}, "expected": 0},
            {"input": {"text1": "abcba", "text2": "abcbcba"}, "expected": 5},
            {"input": {"text1": "bl", "text2": "yby"}, "expected": 1},
            {"input": {"text1": "oxcpqrsvwf", "text2": "shmtulqrypy"}, "expected": 2},
            {"input": {"text1": "ezupkr", "text2": "ubmrapg"}, "expected": 2}
        ],
        "tags": ["string", "dynamic-programming"],
        "companies": ["amazon", "google"],
        "frequency": "medium",
        "category": "blind75"
    },
    # --- Matrix ---
    {
        "id": "set-matrix-zeroes",
        "title": "Set Matrix Zeroes",
        "difficulty": "medium",
        "description": "Given an `m x n` integer matrix, if an element is `0`, set its entire row and column to `0`'s.\n\nYou must do it in place.",
        "examples": [
            {"input": "matrix = [[1,1,1],[1,0,1],[1,1,1]]", "output": "[[1,0,1],[0,0,0],[1,0,1]]", "explanation": ""},
            {"input": "matrix = [[0,1,2,0],[3,4,5,2],[1,3,1,5]]", "output": "[[0,0,0,0],[0,4,5,0],[0,3,1,0]]", "explanation": ""}
        ],
        "constraints": ["m == matrix.length", "n == matrix[0].length", "1 <= m, n <= 200"],
        "starter_code": {
            "python": "def set_zeroes(matrix: list[list[int]]) -> list[list[int]]:\n    # Modify in place and return\n    # Your code here\n    return matrix",
            "javascript": "function setZeroes(matrix) {\n    // Modify in place and return\n    // Your code here\n    return matrix;\n}",
            "java": "import java.util.*;\n\npublic class Solution {\n    public static int[][] setZeroes(int[][] matrix) {\n        // Your code here\n        return matrix;\n    }\n\n    public static void main(String[] args) {\n        int[][] m = {{1,1,1},{1,0,1},{1,1,1}};\n        int[][] result = setZeroes(m);\n        for (int[] row : result) System.out.println(Arrays.toString(row));\n    }\n}"
        },
        "test_cases": [
            {"input": {"matrix": [[1,1,1],[1,0,1],[1,1,1]]}, "expected": [[1,0,1],[0,0,0],[1,0,1]]},
            {"input": {"matrix": [[0,1,2,0],[3,4,5,2],[1,3,1,5]]}, "expected": [[0,0,0,0],[0,4,5,0],[0,3,1,0]]},
            {"input": {"matrix": [[1]]}, "expected": [[1]]},
            {"input": {"matrix": [[0]]}, "expected": [[0]]},
            {"input": {"matrix": [[1,0],[0,1]]}, "expected": [[0,0],[0,0]]},
            {"input": {"matrix": [[1,2,3],[4,5,6]]}, "expected": [[1,2,3],[4,5,6]]},
            {"input": {"matrix": [[1,0,3]]}, "expected": [[0,0,0]]},
            {"input": {"matrix": [[1],[0],[3]]}, "expected": [[0],[0],[0]]}
        ],
        "tags": ["array", "matrix", "hash-table"],
        "companies": ["amazon", "meta", "microsoft"],
        "frequency": "medium",
        "category": "blind75"
    },
    {
        "id": "spiral-matrix",
        "title": "Spiral Matrix",
        "difficulty": "medium",
        "description": "Given an `m x n` matrix, return all elements of the matrix in spiral order.",
        "examples": [
            {"input": "matrix = [[1,2,3],[4,5,6],[7,8,9]]", "output": "[1,2,3,6,9,8,7,4,5]", "explanation": ""},
            {"input": "matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]", "output": "[1,2,3,4,8,12,11,10,9,5,6,7]", "explanation": ""}
        ],
        "constraints": ["m == matrix.length", "n == matrix[i].length", "1 <= m, n <= 10"],
        "starter_code": {
            "python": "def spiral_order(matrix: list[list[int]]) -> list[int]:\n    # Your code here\n    pass",
            "javascript": "function spiralOrder(matrix) {\n    // Your code here\n}",
            "java": "import java.util.*;\n\npublic class Solution {\n    public static List<Integer> spiralOrder(int[][] matrix) {\n        // Your code here\n        return new ArrayList<>();\n    }\n\n    public static void main(String[] args) {\n        System.out.println(spiralOrder(new int[][]{{1,2,3},{4,5,6},{7,8,9}}));\n    }\n}"
        },
        "test_cases": [
            {"input": {"matrix": [[1,2,3],[4,5,6],[7,8,9]]}, "expected": [1,2,3,6,9,8,7,4,5]},
            {"input": {"matrix": [[1,2,3,4],[5,6,7,8],[9,10,11,12]]}, "expected": [1,2,3,4,8,12,11,10,9,5,6,7]},
            {"input": {"matrix": [[1]]}, "expected": [1]},
            {"input": {"matrix": [[1,2],[3,4]]}, "expected": [1,2,4,3]},
            {"input": {"matrix": [[1,2,3]]}, "expected": [1,2,3]},
            {"input": {"matrix": [[1],[2],[3]]}, "expected": [1,2,3]},
            {"input": {"matrix": [[1,2],[3,4],[5,6]]}, "expected": [1,2,4,6,5,3]},
            {"input": {"matrix": [[1,2,3,4]]}, "expected": [1,2,3,4]}
        ],
        "tags": ["array", "matrix", "simulation"],
        "companies": ["amazon", "google", "meta", "microsoft"],
        "frequency": "high",
        "category": "blind75"
    },
    # --- Linked List (remaining) ---
    {
        "id": "remove-nth-node-from-end",
        "title": "Remove Nth Node From End of List",
        "difficulty": "medium",
        "description": "Given the `head` of a linked list, remove the `nth` node from the end of the list and return its head.",
        "examples": [
            {"input": "head = [1,2,3,4,5], n = 2", "output": "[1,2,3,5]", "explanation": ""},
            {"input": "head = [1], n = 1", "output": "[]", "explanation": ""}
        ],
        "constraints": ["The number of nodes is sz", "1 <= sz <= 30", "0 <= Node.val <= 100", "1 <= n <= sz"],
        "starter_code": {
            "python": "def remove_nth_from_end(head: list[int], n: int) -> list[int]:\n    # Your code here\n    pass",
            "javascript": "function removeNthFromEnd(head, n) {\n    // Your code here\n}",
            "java": "import java.util.*;\n\npublic class Solution {\n    public static int[] removeNthFromEnd(int[] head, int n) {\n        // Your code here\n        return new int[]{};\n    }\n\n    public static void main(String[] args) {\n        System.out.println(Arrays.toString(removeNthFromEnd(new int[]{1,2,3,4,5}, 2)));\n    }\n}"
        },
        "test_cases": [
            {"input": {"head": [1,2,3,4,5], "n": 2}, "expected": [1,2,3,5]},
            {"input": {"head": [1], "n": 1}, "expected": []},
            {"input": {"head": [1,2], "n": 1}, "expected": [1]},
            {"input": {"head": [1,2], "n": 2}, "expected": [2]},
            {"input": {"head": [1,2,3], "n": 1}, "expected": [1,2]},
            {"input": {"head": [1,2,3], "n": 3}, "expected": [2,3]},
            {"input": {"head": [1,2,3,4,5], "n": 5}, "expected": [2,3,4,5]},
            {"input": {"head": [1,2,3,4,5], "n": 1}, "expected": [1,2,3,4]}
        ],
        "tags": ["linked-list", "two-pointers"],
        "companies": ["amazon", "meta", "google"],
        "frequency": "high",
        "category": "blind75"
    },
    {
        "id": "reorder-list",
        "title": "Reorder List",
        "difficulty": "medium",
        "description": "You are given the head of a singly linked-list. The list can be represented as:\n`L0 -> L1 -> ... -> Ln-1 -> Ln`\n\nReorder the list to be:\n`L0 -> Ln -> L1 -> Ln-1 -> L2 -> Ln-2 -> ...`\n\nYou may not modify the values in the list's nodes. Only nodes themselves may be changed.",
        "examples": [
            {"input": "head = [1,2,3,4]", "output": "[1,4,2,3]", "explanation": ""},
            {"input": "head = [1,2,3,4,5]", "output": "[1,5,2,4,3]", "explanation": ""}
        ],
        "constraints": ["Number of nodes is in range [1, 5 * 10^4]", "1 <= Node.val <= 1000"],
        "starter_code": {
            "python": "def reorder_list(head: list[int]) -> list[int]:\n    # Your code here\n    pass",
            "javascript": "function reorderList(head) {\n    // Your code here\n}",
            "java": "import java.util.*;\n\npublic class Solution {\n    public static int[] reorderList(int[] head) {\n        // Your code here\n        return new int[]{};\n    }\n\n    public static void main(String[] args) {\n        System.out.println(Arrays.toString(reorderList(new int[]{1,2,3,4})));\n    }\n}"
        },
        "test_cases": [
            {"input": {"head": [1,2,3,4]}, "expected": [1,4,2,3]},
            {"input": {"head": [1,2,3,4,5]}, "expected": [1,5,2,4,3]},
            {"input": {"head": [1]}, "expected": [1]},
            {"input": {"head": [1,2]}, "expected": [1,2]},
            {"input": {"head": [1,2,3]}, "expected": [1,3,2]},
            {"input": {"head": [1,2,3,4,5,6]}, "expected": [1,6,2,5,3,4]},
            {"input": {"head": [1,2,3,4,5,6,7]}, "expected": [1,7,2,6,3,5,4]}
        ],
        "tags": ["linked-list", "two-pointers", "stack"],
        "companies": ["amazon", "meta", "google"],
        "frequency": "medium",
        "category": "blind75"
    },
]


def main():
    with open(DATA_PATH) as f:
        questions = json.load(f)

    existing_ids = {q["id"] for q in questions}
    added = 0

    for q in NEW_QUESTIONS:
        if q["id"] not in existing_ids:
            questions.append(q)
            added += 1
            print(f"  + {q['id']} ({q['difficulty']})")
        else:
            print(f"  = {q['id']} (already exists)")

    with open(DATA_PATH, "w") as f:
        json.dump(questions, f, indent=2)

    print(f"\nAdded {added} new questions. Total: {len(questions)}")


if __name__ == "__main__":
    main()
