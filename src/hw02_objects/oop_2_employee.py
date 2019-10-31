"""
Exercise 2: (4 points)

a) Write the complete code for the Employee class
    (including constructor, __str__,...). (2 points)

b) Create a few employee objects and show how you can
    manipulate them using the methods. (1 point)

c) Draw a UML class diagram for your Employee class. (1 point)
"""


class Employee:
    number_of_employees = 0
    holidays = bool
    # CONSTRUCTOR
    def __init__(self, firstName, lastName, department, idNum, lohn, working_hours):
      self.firstName = firstName
      self.lastName = lastName
      self.department = department
      self.idNum = idNum
      self.lohn = lohn
      self.working_hours = working_hours
      Employee.number_of_employees += 1
    
    # prints information about the number of employees
    @staticmethod
    def employees_info():
      print(str(Employee.number_of_employees) + " employees work in our company " )
    
    # String representation of an object:
    # the method resturs string that describes an employee
    def __str__(self):
      result = "*** Employee INFO ***\n"
      result += "Employee's first name is " + self.firstName + ".\n"
      result += "Employee's last name is " + self.lastName + ".\n"
      result += "Employee's ID number is " + str(self.idNum) + ".\n"
      result += "Employee " + self.firstName + " " + self.lastName + " " + "works at " + self.department + " department."
      return result

    # Sets new department
    def set_department(self,new_department):
      if (not type(new_department) == str):
        raise TypeError
      self.department = new_department

    # Setting new ID number
    def set_idnumber(self,new_idnumber):
      self.idNum = new_idnumber

    # Sets new amount of working hours
    def set_working_hours(self,hours):
      self.working_hours = hours
  
    def holidays_requirement(self):
      if self.working_hours > 40:
        Employee.holidays = True
        print("The worker " + self.lastName + " can have a vacation")


if __name__ == "__main__":
    print("Employee application")
    employee1 = Employee("Tim","Gehry","IT",2345,800,40)
    employee2 = Employee("Sara","Navich","Marketing",8765, 500, 60)

    print(employee1)
    employee1.set_department("IT Management")
    employee1.set_idnumber(4578)
    print(employee1)
    Employee.employees_info()
 
    print(employee2)
    employee2.holidays_requirement()
