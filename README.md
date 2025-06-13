# Inventory Management System  

## Overview  
A comprehensive **web-based inventory management system** built with Python (Flask) and SQL Server. The system helps businesses track products, categories, and transactions while generating insightful reports like low stock alerts and inventory valuation.  

## Features  

### Core Modules  
- **Product Management**  
  - Add/edit/delete products with details (name, price, quantity, supplier, etc.)  
  - Search functionality  
- **Category Management**  
  - Organize products into categories  
- **Transaction Processing**  
  - Record purchases, sales, transfers, and adjustments  
  - Track customer and location data  
- **Reporting**  
  - Low stock alerts  
  - Inventory valuation  
  - Transaction history  

### Technical Highlights  
- **Frontend**: Bootstrap 4 for responsive UI  
- **Backend**: Flask (Python) with SQL Server database  
- **Security**: Parameterized queries to prevent SQL injection  
- **Modular Design**: Clean separation of templates and routes  

## Setup & Installation  

1. **Prerequisites**:  
   - Python 3.x  
   - SQL Server  
   - `pip install flask pyodbc`  

2. **Database Configuration**:  
   - Update `SERVER`, `DATABASE`, and `DRIVER` in `app.py`  

3. **Run the Application**:  
   ```bash  
   python app.py  
   ```  
   Access at: `http://localhost:5000`  

## Screenshots  
| Module | Preview |  
|--------|---------|  
| Products | ![Products Page](https://via.placeholder.com/400x200?text=Products+List) |  
| Transactions | ![Transactions Page](https://via.placeholder.com/400x200?text=Transactions) |  
| Low Stock Report | ![Report](https://via.placeholder.com/400x200?text=Low+Stock+Alert) |  

## File Structure  
```  
├── app.py               # Flask application (routes + DB logic)  
├── templates/           # HTML templates  
│   ├── products.html    # Product listing  
│   ├── transactions.html # Transaction history  
│   └── reports/         # Report templates  
└── README.md  
```  

## Future Enhancements  
- **User Authentication**: Role-based access control  
- **Barcode Integration**: Scan products via barcode  
- **REST API**: For mobile/third-party integrations  

Developed as a practical project for inventory management coursework.  

--- 
