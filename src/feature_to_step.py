from statement import Statement


def main():
    feature = "project_creation"
    with open(f"./features/{feature}.feature", "r") as file, open(f"{feature}.steps.ts", "w") as outfile:
        outfile.write('import { Given, When, Then, TableDefinition } from "cucumber";\n\n\n')
        antecessors = []
        previous_patterns = {
            "Given": [],
            "When": [],
            "Then": [],
        }

        for line in file.readlines():
            statement = Statement.for_line(line, outfile)
            if statement:
                statement.write_statement_block(antecessors, previous_patterns)


if __name__ == '__main__':
    main()
