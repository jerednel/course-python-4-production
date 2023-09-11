def even_numbers(n):
    for i in range(n):
        yield 2*i

# Example usage
for num in even_numbers(5):
    print(num)