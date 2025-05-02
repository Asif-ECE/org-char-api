# OrgChartProject

OrgChartProject is a simple and efficient API for managing organizational charts. It allows users to create, update, and retrieve hierarchical structures of employees or departments.

## Features

- Create and manage organizational charts.
- Add, update, and delete nodes (employees or departments).
- Retrieve hierarchical data in JSON format.
- Lightweight and easy to integrate.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/OrgChartProject.git
    ```
2. Navigate to the project directory:
    ```bash
    cd OrgChartProject
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Start the server:
    ```bash
    uvicorn main:app --reload
    ```
2. Access the API at `http://localhost:8000`.

### API Endpoints

#### 1. Create an Employee
- **Endpoint**: `POST /org_charts/{org_id}/employees/`
- **Description**: Adds a new employee to the organizational chart.
- **Request Body**:
  ```json
  {
     "name": "John Doe",
     "manager_id": "123"
  }
  ```
- **Response**:
  ```json
  {
     "id": "456",
     "name": "John Doe",
     "manager_id": "123"
  }
  ```

#### 2. Get All Employees in an Organization
- **Endpoint**: `GET /org_charts/{org_id}/employees/`
- **Description**: Retrieves all employees in a specific organization.
- **Response**:
  ```json
  [
     {
        "id": "123",
        "name": "Jane Smith",
        "manager_id": null
     }
  ]
  ```

#### 3. Get an Employee by ID
- **Endpoint**: `GET /org_charts/{org_id}/employees/{id}/`
- **Description**: Retrieves details of a specific employee.
- **Response**:
  ```json
  {
     "id": "123",
     "name": "Jane Smith",
     "manager_id": null
  }
  ```

#### 4. Update an Employee's Manager
- **Endpoint**: `PUT /org_charts/{org_id}/employees/{id}/`
- **Description**: Updates the manager of a specific employee.
- **Request Body**:
  ```json
  {
     "new_manager_id": "789"
  }
  ```
- **Response**:
  ```json
  {
     "id": "123",
     "name": "Jane Smith",
     "manager_id": "789"
  }
  ```

#### 5. Delete an Employee
- **Endpoint**: `DELETE /org_charts/{org_id}/employees/{id}/`
- **Description**: Deletes an employee from the organizational chart.
- **Response**:
  ```json
  {
     "detail": "Employee deleted successfully"
  }
  ```

#### 6. Promote an Employee to CEO
- **Endpoint**: `POST /org_charts/{org_id}/employees/{id}/promote`
- **Description**: Promotes an employee to the CEO position.
- **Response**:
  ```json
  {
     "id": "123",
     "name": "Jane Smith",
     "manager_id": null
  }
  ```

## Technologies Used

- FastAPI
- SQLModel
- Alembic

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch:
    ```bash
    git checkout -b feature-name
    ```
3. Commit your changes:
    ```bash
    git commit -m "Add feature-name"
    ```
4. Push to the branch:
    ```bash
    git push origin feature-name
    ```
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, please contact:
- **Name**: Asif
- **Email**: md.asif.mostafa@outlook.com
