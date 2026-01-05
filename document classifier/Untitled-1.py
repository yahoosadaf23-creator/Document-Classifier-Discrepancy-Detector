def greet(name):
    """Return a greeting message."""
    return f"Hello, {name}!"

def main():
    # Variables
    name = "World"
    age = 20

    # Function call
    message = greet(name)
    print(message)

    # Conditional
    if age >= 18:
        print("You are an adult.")
    else:
        print("You are a minor.")

    # Loop
    print("Counting:")
    for i in range(1, 6):
        print(i)

# Entry point
if __name__ == "__main__":
    main()
