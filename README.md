# Monthly Budget Tracker Application

A **Streamlit** application designed to help users track and manage their monthly budgets, providing an easy-to-use interface to monitor income, expenses, and savings goals. The app is deployed using **AWS ECS**, **ECR**, and **Auto Scaling** to handle varying traffic loads efficiently. The setup also utilizes **Terraform** and **GitHub Actions** for CI/CD automation.

---

## Features

- **Track Monthly Budget**: Users can input income and expense categories and track their budget for the month.
- **Financial Summary**: Displays a visual summary of the user's financial situation, including graphs to illustrate the budget breakdown.
- **Goal Setting**: Allows users to set financial goals and track their progress over time.
- **Responsive Interface**: Built with Streamlit for an interactive and responsive web application.

---

## Application URL

The application is deployed on **AWS ECS** with an **Application Load Balancer (ALB)**. You can access it here:

[Streamlit Budget Tracker](http://budget-tracking-alb-563686057.ap-south-1.elb.amazonaws.com/)

---

## Prerequisites

Before running or deploying the application, make sure you have the following installed:

1. **AWS Account**: Required to deploy resources on AWS.
2. **Terraform**: To manage infrastructure as code.
3. **Docker**: To build and push Docker images to Amazon ECR.
4. **Streamlit**: For building the web application.
5. **GitHub Account**: For managing the repository and automating deployments using GitHub Actions.

---

## Infrastructure Setup

The infrastructure for this application is managed using **Terraform**. It creates the necessary AWS resources such as:

- **ECS Cluster**: To host the Streamlit application.
- **ECR Repository**: To store the Docker image of the app.
- **Auto Scaling**: Ensures that the application scales based on CPU and memory usage.
- **ALB**: Provides an entry point to access the application.

### Steps to Deploy:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/MrinalBhoumick/monthly-budget-tracker-application.git
   cd monthly-budget-tracker-application
   ```

2. **Install Terraform**:
   Ensure you have **Terraform** installed and configured for your AWS account. If you don't have it installed, follow the official [Terraform installation guide](https://learn.hashicorp.com/tutorials/terraform/install-cli).

3. **Configure AWS CLI**:
   Make sure the AWS CLI is set up with the necessary permissions. You can configure the AWS CLI by running:
   ```bash
   aws configure
   ```

4. **Terraform Initialization**:
   Initialize Terraform in the project directory:
   ```bash
   terraform init
   ```

5. **Apply Terraform Configuration**:
   Run the following command to apply the infrastructure:
   ```bash
   terraform apply
   ```

6. **Deploy Streamlit Application**:
   The application code is already set up in the repository. To deploy it, ensure you have Docker installed and use the following commands:

   - Build the Docker image:
     ```bash
     docker build -t streamlit-budget-tracker .
     ```

   - Tag the Docker image:
     ```bash
     docker tag streamlit-budget-tracker:latest <aws_account_id>.dkr.ecr.<region>.amazonaws.com/streamlit-app-repo:latest
     ```

   - Push the Docker image to ECR:
     ```bash
     aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<region>.amazonaws.com
     docker push <aws_account_id>.dkr.ecr.<region>.amazonaws.com/streamlit-app-repo:latest
     ```

7. **Access the Streamlit Application**:
   Once the Docker image is pushed to **Amazon ECR**, the ECS service will be updated, and you can access the Streamlit application at the provided ALB URL.

---

## Auto Scaling Setup

The application is configured with **auto scaling** to automatically adjust the number of running instances based on the CPU and memory utilization. 

### ECS Service Auto Scaling Configuration:

- **CPU Scaling Policy**: Scales up or down based on average CPU utilization.
- **Memory Scaling Policy**: Scales based on average memory usage.

---

## CI/CD Pipeline with GitHub Actions

The deployment process is automated using **GitHub Actions**, ensuring seamless updates to the application. The CI/CD pipeline includes the following steps:

1. **Build Docker Image**: On each push to the `main` branch, GitHub Actions builds the Docker image from the repository.
2. **Push to ECR**: The image is pushed to the **Amazon ECR** repository.
3. **Deploy to ECS**: The image is deployed to **AWS ECS**, and the service is updated to reflect the latest version.

You can view the **GitHub Actions workflow** for deployment in the `.github/workflows/ci-cd.yml` file in this repository.

---

## How to Contribute

If you’d like to contribute to the development of this application, follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request to merge your changes into the `main` branch.

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## Conclusion

By following this guide, we have successfully deployed the **Monthly Budget Tracker** application using **AWS ECS**, **ECR**, and **auto scaling**. With **Terraform** and **GitHub Actions**, you now have a fully automated deployment pipeline for seamless updates and scaling.

For further information or to report issues, please visit the **GitHub Repository**:

[GitHub Repository](https://github.com/MrinalBhoumick/monthly-budget-tracker-application.git)