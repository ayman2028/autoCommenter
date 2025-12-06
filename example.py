"""
Example script to test Auto Commenter with local LLM.
This demonstrates the kinds of code that get commented.
"""

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)


def merge_sorted_lists(list1, list2):
    result = []
    i, j = 0, 0
    
    while i < len(list1) and j < len(list2):
        if list1[i] <= list2[j]:
            result.append(list1[i])
            i += 1
        else:
            result.append(list2[j])
            j += 1
    
    result.extend(list1[i:])
    result.extend(list2[j:])
    return result


class DataProcessor:
    def __init__(self, data):
        self.data = data
        self.processed = False
    
    def validate(self):
        if not self.data:
            return False
        if not isinstance(self.data, list):
            return False
        return all(isinstance(item, str) for item in self.data)
    
    def process(self):
        if not self.validate():
            print("Invalid data format")
            return None
        
        self.data = [item.strip().lower() for item in self.data if item.strip()]
        self.processed = True
        return self.data
    
    def filter_by_length(self, min_length):
        if not self.processed:
            self.process()
        
        return [item for item in self.data if len(item) >= min_length]
    
    def filter_by_prefix(self, prefix):
        if not self.processed:
            self.process()
        
        return [item for item in self.data if item.startswith(prefix)]


def calculate_statistics(numbers):
    if not numbers:
        return None
    
    total = sum(numbers)
    average = total / len(numbers)
    minimum = min(numbers)
    maximum = max(numbers)
    
    return {
        'sum': total,
        'average': average,
        'min': minimum,
        'max': maximum,
        'count': len(numbers)
    }


def main():
    fib_result = fibonacci(10)
    print(f"Fibonacci(10) = {fib_result}")
    
    list1 = [1, 3, 5, 7]
    list2 = [2, 4, 6, 8]
    merged = merge_sorted_lists(list1, list2)
    print(f"Merged: {merged}")
    
    processor = DataProcessor(["Hello", "World", "Python", "Local", "LLM"])
    processed = processor.process()
    print(f"Processed: {processed}")
    
    filtered = processor.filter_by_length(5)
    print(f"Items with length >= 5: {filtered}")
    
    numbers = [10, 20, 30, 40, 50]
    stats = calculate_statistics(numbers)
    print(f"Statistics: {stats}")


if __name__ == "__main__":
    main()
