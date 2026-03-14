# Odin
Project, Computer Science

## Project Description
An Autonomous cloud infrastructure management system for monitoring analysing and responding to operational events, ensuring reliaablity, scalability and resilience across multiple cloud instances

## Installation Instructions
AWS account required with a vpc built containing autoscaled EC2 instances behind a loadbalancer, another EC2 instance with mongodb installed (database instance is not compulsory).

OpenAI account required as an OpenAI key will be needed.

.env file required with the following parameters:

cookie_name
cookie_password
db=mongodb://XXX.XXX.XXX.XXX:27017/ODIN?directConnection=true
cloudinary_name
cloudinary_key
cloudinary_secret
OPENAI_API_KEY
dbIp
sIp
bastion

## Usage
1. Clone this repository and install node.js and run it via npm start
2. Sign up with Email and password.
3. Use Dashboard to monitor EC2 instances metrics
4. Odin's Comment suggest the overall health of th instances.
5. History button at the top right shows all the comments Odin has mentioned.
6. Use Settings to change account details or delete or change the password for another account.
    
## Configuration
N/A

## Examples
N/A

## Documentation
N/A

## Contributing Guidelines
N/A

## License
N/A

## Contact Information
Not available

## Acknowledgements
Github account: techwithtim
Github: PythonAIAgentin10Minutes




