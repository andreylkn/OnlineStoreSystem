def input_bool(prompt):
    while True:
        val = input(prompt + " (y/n): ").strip().lower()
        if val in ['y', 'yes']:
            return True
        elif val in ['n', 'no']:
            return False
        else:
            print("Invalid choice. Enter 'y' or 'n'.")
