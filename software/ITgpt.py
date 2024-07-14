from regressor import ITgpt

id = int(input("Enter the asset ID: "))
name = input("Enter the asset Name: ")

print('1. Firewall')
print('2. Router')
print('3. Server')
print('4. Switch')
print('5. Workstation')
asset_type = int(input('Enter the number: ')) - 1

cost = float(input("Enter the cose: "))

print('1. Data center 1')
print('2. Data center 2')
print('3. Office 1')
print('4. Office 2')
print('5. Remote Site')
location = int(input("Enter the location number: ")) - 1

print('4. IBM     ')
print('3. HP      ')
print('5. Juniper ')
print('1. Cisco   ')
print('2. Dell     ')
manu = int(input("Enter the manufacturer number: ")) - 1

print('1. Finance')
print('2. Operations')
print('3. HR')
print('4. Engineering')
print('5. IT')
dept = int(input("Enter the department number: ")) - 1

print('1. In maintenance')
print('2. Retired')
print('3. In use')
status = int(input("Enter the Status number: ")) - 1

print('1. Jane Smith') 
print('2. Alice Brown ')
print('3. Bob Johnson ')
print('4. John Doe ')
print('5. Charlie Davis ')
assigned = int(input("Enter the person who is assigned: "))-1

days_from_purchase = int(input("Enter the number of days from purchase: "))
days_from_expiry = int(input("Enter the number of days from expiry: "))

dict = {
    'asset_id':[id],
    'asset_name':[name],
    'asset_type':[asset_type],
    'manufacturer':[manu],
    'cost':[cost],'location':[location],
    'department':[dept],
    'asset_status':[status],
    'assigned_to':[assigned], 
    'days_from_purchase':[days_from_purchase],
    'days_to_warranty_expiry':[days_from_expiry] 
}

ai = ITgpt()
maintenance_cost = ai.maintenance_cost('cost',dict)
maintenance_day = ai.next_maintenance('cost',dict)

print(f'The maintenance for the product should done at next {maintenance_day}, and the predicted cost is {maintenance_cost}')