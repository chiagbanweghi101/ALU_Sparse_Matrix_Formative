from sparseMatrix import SparseMatrix
import os

def get_base_name(filepath):
    """Returns the base filename without extension"""
    return os.path.splitext(os.path.basename(filepath))[0]

def result_filename(op_name, file1, file2):
    """Constructs result filename for the output matrix"""
    name1 = get_base_name(file1)
    name2 = get_base_name(file2)

    if op_name == "Subtraction":
        filename = f"{op_name}_{name1}_minus_{name2}.txt"
    else:
        filename = f"{op_name}_{name1}_and_{name2}.txt"

    return filename


def main():
    print("\n Sparse Matrix Operations:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")

    choosen_operation = input("\nChoose operation (1, 2, 3): ").strip()
    if choosen_operation not in ['1', '2', '3']:
        print("Invalid selection. Exiting program.")
        return


    # Get input file paths
    first_file = input("input the path to first matrix file: ").strip()
    second_file = input("input the path to second matrix file: ").strip()

    # Check if files exist
    if not os.path.exists(first_file) or not os.path.exists(second_file):
        print("Error: One or both matrix files do not exist.")
        return

    # Load matrices (will raise if invalid, that's OK)
    first_matrix = SparseMatrix(sample_file=first_file)
    second_matrix = SparseMatrix(sample_file=second_file)

    # Create output directory
    results_dir = 'results'
    os.makedirs(results_dir, exist_ok=True)

    # Select operation
    operation_map = {
        '1': ("Addition", first_matrix.add),
        '2': ("Subtraction", first_matrix.subtract),
        '3': ("Multiplication", first_matrix.multiply)
    }

    op_name, operation_func = operation_map[choosen_operation]
    result_matrix = operation_func(second_matrix)

    # Write result
    output_filename = result_filename(op_name, first_file, second_file)
    output_path = os.path.join(results_dir, output_filename)
    result_matrix.write_to_file(output_path)

    print(f"\nSuccessful. check output in this file: {output_path}")


if __name__ == "__main__":
    main()
