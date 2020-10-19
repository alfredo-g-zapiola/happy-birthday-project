# Happy_birthday_project

Happy Birthday Project
## About

Cloud infrastructure to send automatic happy birthay emails on AWS:


Project structure:

```bash
weekly_ore_email_project     <-- The high level project directory
├── README.md                               <-- This instructions file
├── .gitignore                              <-- Git ignore file
├── deploy_template                         <-- Directory for AWS packaged objects
│   └── packaged.yaml                       <-- Directions for a Packaged Lambda function
├── weekly_ore_email         <-- Source code for a lambda function
│   ├── __init__.py
│   ├── weekly_ore_email.py  <-- Lambda function code
s│   └── requirements.txt                    <-- Python dependencies
├── template.yaml                           <-- SAM Template
└── tests                                   <-- Unit tests
    ├── test_data                           <-- Test data used in the tests
        └── sample_event.json
    └── unit
        ├── __init__.py
        └── test_handler.py
```

Detailed description of each item above:
* *High level project directory*: This contains all of the code and the files required for this particular Lambda function.
* *README.md*: The file that you're currently reading. Contains all of the instructions for how to start up a new project, test it locally, deploy it to AWS and test it on AWS.
* *.gitignore*: Standard template for .gitignore that has additional criteria for AWS projects as well as Pycharm.
* *deploy_template*: A directory for storing the instruction files needed to deploy a Lambda function. AWS will build the Lambda function and store the information needed to deploy it in this directory. Note - this directory is used as an argument below when packaging a project.
* *packaged.yaml*: This file will not exist until you package a Lambda.
* *weekly_ore_email*: Directory that contains all of the code, configs, requirements, etc. needed to package the Lambda function and load it into AWS. AWS requires that a "flat" folder structure be used for all Python Lambda functions and this acts as the base for that structure.
* *weekly_ore_email.py*: The file that contains all of the code to execute for the Lambda.
* *template.yaml*: This file is a template that AWS uses in order to build the packaged Lambda file which can be deployed.
* *tests*: Contains all of the tests, note that for this example the test data can be used when invoking and manually testing a Lambda function in addition to being used as part of automated tests.

# Development

This project should run, as is. Changes can be made to the `weekly_ore_email/weekly_ore_email.py` file to update the functionality. In addition, requirements should be added to the `weekly_ore_email/requirements.txt` file. Amazon manages the version of Python on their own and since Lambda is a managed service Amazon will push out updates to base Python packages on their own. Because of this it is a best practice to always provide the version of the requirements packages needed (`pip freeze` can be run to get the current version of all requirements).

## Setup process

### Building the project

[AWS Lambda requires a flat folder](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html) with the application as well as its dependencies. When you make changes to your source code or dependency manifest,
run the following command to build your project local testing and deployment:

#### NOTE - it is assumed that ALL of these commands are executed from the weekly_ore_email_project directory. They can be executed elsewhere but the paths to the files will need to be added manually.

Always use the container flag to ensure that the environment testing with matches the AWS Lambda environment.
```bash
sam build --use-container
```
By default, this command writes built artifacts to `.aws-sam/build` folder.

This builds a docker container with your packages installed. By using the `sam` command, interacting with the docker container is seamless. This docker container also matches the exact container that AWS runs in production.

# To test
Execute from the project's top level directory.
```bash
sam local invoke --event tests/test_data/sample_event.json
```

## Packaging and deployment
After a package is created it needs to be uploaded into S3 in order to allow it to be imported as a Lambda function.

If an S3 bucket has not already been created, create one.
NOTE: This S3 bucket should already be created and is used for hosting code. If possible do not create extra buckets.
```bash
aws s3 mb s3://some-bucket-name
```

Next, run the following command to package our Lambda function to S3:

```bash
sam package \
    --output-template-file deploy_template/packaged.yaml \
    --s3-bucket some-bucket-name
```

When you run this command you will see something similar to this output:
```bash
Uploading to 629073b4e73f19232ec62e10edc9231e 6345854 / 6345854.0  (100.00%)
Successfully packaged artifacts and wrote output template to file deploy_template/packaged.yaml.
Execute the following command to deploy the packaged template
```
If you decide to manually upload the Lambda in the following steps then you will need the value that looks like *629073b4e73f19232ec62e10edc9231e*, this is the object key for the Lambda function.

Next, the following command will create a CloudFormation Stack and deploy your SAM resources. Note - if the role is not provided as part of the template/packaged YAML you will need to add it through the GUI.

You do not have to deploy this code through the command line, it can also be uploaded through the GUI as a Lambda function. Just provide the S3 bucket and object name that AWS created when the object was packaged.

```bash
sam deploy \
    --template-file deploy_template/packaged.yaml \
    --stack-name weekly_ore_email
```
If the command line was used to deploy the code it will create a stack, you may want to update the stack name above.

After deployment is complete you can run the following command to retrieve the outputs as defined in the template, pass in the same stack name as above:

```bash
aws cloudformation describe-stacks \
    --stack-name weekly_ore_email \
    --query 'Stacks[].Outputs'
```


## Testing

**Pytest** and **pytest-mock** are used for testing our code and you can install it using pip: ``pip install pytest pytest-mock``

It is a best practice to execute this as virtual environment. One virtual environment for each Lambda function is best practice, however, for groupings of Lambda functions that have the same or very similar requirements one virtual environment should be fine.

Next, to execute the tests run the following:

```bash
PYTHONPATH=weekly_ore_email/ pytest -vvv
```

Next, we run `pytest` against our `tests` folder to run our initial unit tests from within the package directory. Since there are additional packages for the Lambda within the same "flat" directory, they must be added to the path as well (AWS Lambda does this automatically):

```bash
PYTHONPATH=$PWD/update_blacklist python -m pytest tests -v   
```


# Appendix


> **See [Serverless Application Model (SAM) HOWTO Guide](https://github.com/awslabs/serverless-application-model/blob/master/HOWTO.md) for more details in how to get started.**
