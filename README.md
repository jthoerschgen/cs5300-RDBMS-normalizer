# CS 5300 - Programming Project: RDBMS Normalizer

## *Errors in Sample Data* - Corrections

### OrderID -> PromoCodeUsed

- Not 2NF violation, is actually a BCNF violation

### DrinkID -> DrinkName

- corrected, is a PFD violation

### FoodID -> FoodName

- corrected, is a PFD violation

## How To

For decomposing a schema, input an un-normalized relation (type `objects.Relation`) into `rdbms_nomalizer.Normalizer()` and enter the highest desired normal form into the prompt.

For testing run `testing.py` to view individual unit tests for verifying any changes to the code.

## Objective

To develop a program that takes a database (relations) and functional dependencies as input, normalizes the relations based on the provided functional dependencies, produces SQL queries to generate the normalized database tables, and optionally determines the highest normal form of the input table.

![DALL·E 2024-07-12 15.39.52 - A cartoon illustration of a database normalization program. The scene shows a friendly robot sitting at a computer desk, analyzing a large, colorful](DALL·E%202024-07-12%2015.39.52%20-%20A%20cartoon%20illustration%20of%20a%20database%20normalization%20program.%20The%20scene%20shows%20a%20friendly%20robot%20sitting%20at%20a%20computer%20desk,%20analyzing%20a%20large,%20colorful%20f.webp)

## Input Requirements

### Database (Relations)

- This should include the complete set of tables (relations) in the database schema to be normalized. The minimal expected details should include the following:
  - **Table name.**
  - **List of columns** (attributes).
  - **Key constraints** (all primary keys and any candidate keys --- to be used in the *generalized definitions* of 2NF, 3NF, and BCNF).
  - **Any attributes that hold multi-valued, non-atomic data.**
- Since normalization is typically done on individual tables, so your program may choose to handle one table input at a time, which is also acceptable.

### Data Instances

- **Lower Normal Forms:** Most low-level normal forms do not require data instances to be supplied for each relation to perform normalization correctly. They are primarily concerned with the schema structure and the relationships among the attributes using functional dependencies and other provided constraints. Therefore, for normalization from 1NF up to BCNF, your program may implement them WITHOUT input data instances.
  - **4NF:** Moving from lower normal forms to 4NF, which addresses non-trivial multi-valued dependencies, can benefit from examing actual data. For this project:
    1. You may assume that MVDs are provided by the user, detailing the expected independent relationships between attribute groups.
    2. Data instances are REQUIRED ONLY on the relations where MVDs are provided by the user.
    3. Your program must validate these provided MVDs against the actual data instances. If and only if upon successful validation of the MVDs, your program should then perform the necessary decomposition of the relation schema to achieve 4NF.
  - **5NF:** This advanced form of normalization aims to eliminate redundancy caused by join dependencies that are not implied by candidate keys. You will likely need detailed data instances as part of the user input in order to effectively determine any existing join dependencies within the relation table.

### Functional Dependencies

- FDs should be specified in a clear and standard format, typically as a set of attribute names on the left-hand-side (determinant) and right-hand-side (dependent), expressed as **X -> Y** where X and Y represent lists of attributes from the target database schema.

### Additional Constraint Requirements and Assumptions

- For this project, you are NOT required to implement automated testing for detecting "nested relations" as part of the 1NF normalization process.  However, you should ensure that any multi-valued attributes involving fields with non-atomic data are correctly managed. You may include user-provided identification of attributes with non-atomic data as part of the input to your program.

### Choice of the Highest Normal Form to Reach (1NF, 2NF, 3NF, BCNF, 4NF, 5NF)

- Your program is required to allow the user to specify the highest normal form they aim to achieve. When a target normal form is selected, such as 4NF, the program must first ensure that the database meets the criteria for 1NF, 2NF, 3NF, and BCNF in sequence.

**Input Format Flexibility:** You are free to choose the input format and data representations that best suit your approach to the task.

## Output

Upon successfully completing the normalization process, the output of your program should effectively demonstrate the final, normalized database schema. This can be presented in one or more of the following formats to ensure clarity:

1. SQL Queries
    - Provide SQL table definition queries that are ready to execute, which create the normalized tables based on the final schema. These queries should include table creation commands along with appropriate constraints such as primary keys, foreign keys, and any other relevant constraints that were identified during the normalization process.
2. Normalized Relational Database Schema
    - Alternatively, you may output a detailed *schema diagram* or a *textual representation* of the normalized tables. This should include each table's name, list of attributes, and appropriate constraints such as primary keys, foreign keys, and any other relevant constraints that were identified during the normalization process.

## Core Components

1. *Input Parser:* To parse the input dataset and functional dependencies.
2. *Normalizer:* To normalize the dataset based on functional dependencies.
3. *Final Relation Generator:* To generate normalized schema for the database.

## Deliverables

1. *Source Code:* Well-commented source code in the language of your choice.
2. *Code Description:* Detailed documentation describing the flow, logic, and methodology of the code.

## Sample Inputs and Outputs

- Dataset #1: [Download TestingData (1NF-5NF).xlsx](TestingData%20(1NF-5NF).xlsx)

- Dataset #2: [Download TestingData (5NF violation).xlsx](TestingData%20(5NF%20violation).xlsx)

## Extra Credit on Automatic Identification of MVDs (Up to 15 Points)

This is an opportunity to earn extra credit by enhancing your program to *autonomously* identify multi-valued dependencies WITHOUT relying on user-provided MVD data. This would require your program to attempt MVD identification by analyzing the provided data instances only.

The amount of extra credit awarded will be based on the innovation of your approach, the complexity and efficiency of the detection method, and the accuracy of your program in identifying true MVDs within the data.

*Your submission should include a comprehensive report discussing the approach, validation tests performed, challenges faced, and any assumptions made during the normalization process.*

**Students may request a further extension on this extra credit component.**

## Extra Credit on DKNF Implementation (Up to 20 Points)

Students who choose to undertake this challenge will attempt to normalize a given dataset to DKNF, the most stringent form of normalization by ensuring every constraint is a logical consequence of the definition of keys and domains.

Implementing the DKNF is notably challenging and is rarely done in typical database practices due to its complexity and stringent requirements. Therefore, we encourage you to **think outside the box** as you approach this task. Take chances to explore innovative methods and perhaps even develop your own tools or scripts to aid in the normalization process. Keep in mind that one of the key challenges in achieving DKNF is the ability to identify and address hidden constraints that are not explicitly defined through domain or key constraints.

Your creative approach and the insights you gain from attempting to tackle this problem will be used to determine the amount of extra credit awarded.

*Your submission should include a comprehensive report discussing the approach, validation tests performed, challenges faced, and any assumptions made during the normalization process.*

**Students may request a further extension on this extra credit component.**
