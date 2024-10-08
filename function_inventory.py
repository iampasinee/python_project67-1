import struct
import os

# กำหนดโครงสร้างของข้อมูล
PRODUCT_FORMAT = 'I30s30sIf'  # (Product_ID, Product_Name, Product_Category, Product_Quantity, Product_Price)
PRODUCT_SIZE = struct.calcsize(PRODUCT_FORMAT)

class Inventory:
    def __init__(self, file_path):
        self.file_path = file_path

    def _check_product_exists(self, product_id):
        """เช็คว่า product_id มีอยู่ในไฟล์หรือไม่"""
        try:
            with open(self.file_path, 'rb') as file:
                while True:
                    data = file.read(PRODUCT_SIZE)
                    if not data:
                        break
                    product = struct.unpack(PRODUCT_FORMAT, data)
                    if product[0] == product_id:
                        return True
        except FileNotFoundError:
            return False
        return False

    def add_product(self, product_id, product_name, product_category, product_quantity, product_price):

        
        if len(product_name) > 30 or len(product_category) > 30:
            print("Product name and category must not exceed 30 characters!")
            return
        
        # ตั้งค่าหมวดหมู่เป็น "Other" ถ้าไม่มีการกำหนด
        if product_category is None or product_category.strip() == "":
            product_category = "Other"
        
        # เช็คว่ามี product_id ซ้ำหรือไม่
        if self._check_product_exists(product_id):
            print(f"Unable to add product: Product_ID {product_id} already exists!")
            return

        try:
            product_category = product_category.strip().lower().title()  # ทำให้ตัวแรกของแต่ละคำเป็นตัวพิมพ์ใหญ่
            product_name = product_name.strip().lower().title()  # ทำให้ตัวแรกของแต่ละคำเป็นตัวพิมพ์ใหญ่

            with open(self.file_path, 'ab') as file:
                data = struct.pack(PRODUCT_FORMAT, 
                                   product_id,
                                   product_name.encode('utf-8'),
                                   product_category.encode('utf-8'),
                                   product_quantity, 
                                   product_price
                                   )
                file.write(data)
                print("Product added successfully!")

            input("Press Enter to return to the main menu...")  # รอให้ผู้ใช้กด Enter ก่อนที่จะกลับไปที่เมนู

        except Exception as e:
            print(f"An error occurred: {e}")

    def display_products(self):
        try:
            with open(self.file_path, 'rb') as file:
                products = []
                
                # อ่านข้อมูลสินค้าทั้งหมดและเก็บไว้ในรายการ
                while True:
                    data = file.read(PRODUCT_SIZE)
                    if not data:
                        break
                    product = struct.unpack(PRODUCT_FORMAT, data)

                    products.append(product)# เพิ่มสินค้าที่อ่านได้ลงในรายการ

                # เรียงสินค้าตาม ID (ตัวแรกในแต่ละทูเพล)
                products.sort(key=lambda x: x[0])

                print("Display product list:")
                headers = ['ID', 'Name', 'Category', 'Quantity', 'Price(THB)']
                print(f"{headers[0]:<5} {headers[1]:<30} {headers[2]:<30} {headers[3]:<10} {headers[4]:<10}")
                
                for product in products:
                    # แปลงข้อมูลให้ถูกต้อง
                    id_value = product[0]
                    name_value = product[1].decode('utf-8').strip('\x00')
                    category_value = product[2].decode('utf-8').strip('\x00')
                    quantity_value = product[3]
                    price_value = product[4]
                    # แสดงผล
                    print(f"{id_value:<5} {name_value:<30} {category_value:<30} {quantity_value:<10} {price_value:<10,.2f}")
            input("Press Enter to return to the main menu...")  # รอให้ผู้ใช้กด Enter ก่อนที่จะกลับไปที่เมนู

        except FileNotFoundError:
            print("File not found!")
        except Exception as e:
            print(f"An error occurred while displaying the product: {e}")
    
    def generate_inventory_report(self):
        """สร้างรายงานสินค้าที่จัดกลุ่มตามประเภท"""
        try:
            with open(self.file_path, 'rb') as file:
                categories = {}
                
                while True:
                    data = file.read(PRODUCT_SIZE)
                    if not data:
                        break
                    product = struct.unpack(PRODUCT_FORMAT, data)

                    # แปลงข้อมูลให้ถูกต้อง
                    id_value = product[0]
                    name_value = product[1].decode('utf-8').strip('\x00')
                    category_value = product[2].decode('utf-8').strip('\x00')
                    quantity_value = product[3]
                    price_value = product[4]

                    # เพิ่มข้อมูลสินค้าไปยังหมวดหมู่ที่ถูกต้อง
                    if category_value not in categories:
                        categories[category_value] = []
                    categories[category_value].append((id_value, name_value, quantity_value, price_value))

                # แสดงรายงาน
                print(f"\nInventory Report:\nNumber of categories: {len(categories)}\n")

                for category, products in categories.items():
                    total_price = sum(product[2] * product[3] for product in products)  # คำนวณราคารวมของหมวดหมู่

                    print(f"Category : {category}")
                    print(f"Number of Products: {len(products)}")
                    headers = ['ID', 'Name', 'Quantity', 'Price(THB)']
                    print('-'*70)
                    print(f"{headers[0]:<7} {headers[1]:<30} {headers[2]:<10} {headers[3]:<10} ")
                    print('-'*70)

                    for product in products:
                        print(f"{product[0]:03}{'':<4} {product[1]:<30} {product[2]:<10} {product[3]:<10,.2f}")

                    print('-'*70)
                    print(f"Total Price : {total_price:,.2f} THB")  # แสดงราคารวมของหมวดหมู่
                    print('-'*70)
                    print()  # เพื่อให้มีการเว้นบรรทัดระหว่างหมวดหมู่
                
                input("Press Enter to return to the main menu...")  # รอให้ผู้ใช้กด Enter ก่อนที่จะกลับไปที่เมนู
                
        except FileNotFoundError:
            print("File not found!")
        except Exception as e:
            print(f"An error occurred while generating the report: {e}")

    def delete_product(self, product_id):
        """ลบสินค้าจากไฟล์ตาม product_id"""
        temp_file_path = 'temp_inventory.bin'
        product_found = False

        try:
            with open(self.file_path, 'rb') as file, open(temp_file_path, 'wb') as temp_file:
                while True:
                    data = file.read(PRODUCT_SIZE)
                    if not data:
                        break
                    product = struct.unpack(PRODUCT_FORMAT, data)

                    if product[0] == product_id:
                        product_found = True  # เจอสินค้าที่จะลบ
                        continue  # ไม่เขียนสินค้านี้ลงในไฟล์ชั่วคราว
                    
                    temp_file.write(data)   # เขียนสินค้าที่ไม่ถูกลบไปยังไฟล์ชั่วคราว

            if product_found:
                # เปลี่ยนชื่อไฟล์ชั่วคราวเป็นไฟล์หลัก
                import os
                name_value = product[1].decode('utf-8').strip('\x00')
                os.replace(temp_file_path, self.file_path)
                print(f"Product ID {product_id} {name_value} successfully deleted!")
            else:
                os.remove(temp_file_path)  # ลบไฟล์ชั่วคราวถ้าไม่พบสินค้า
                print(f"Product ID {product_id} not found!")

        except FileNotFoundError:
            print("File not found!")
        except Exception as e:
            print(f"An error occurred while deleting the product: {e}")

    def update_product(self, product_id, product_name=None, product_category=None, product_quantity=None, product_price=None):
        """อัปเดตข้อมูลสินค้าตาม product_id"""
        temp_file_path = 'temp_inventory.bin'
        product_found = False

        try:
            with open(self.file_path, 'rb') as file, open(temp_file_path, 'wb') as temp_file:
                while True:
                    data = file.read(PRODUCT_SIZE)
                    if not data:
                        break
                    product = struct.unpack(PRODUCT_FORMAT, data)

                    if product[0] == product_id:
                        product_found = True  # เจอสินค้าที่จะอัปเดต

                        # หากข้อมูลใหม่ถูกระบุ ให้ทำการอัปเดต
                        if product_name is not None:
                            name_encoded = product_name.encode('utf-8')
                        else:
                            name_encoded = product[1]

                        if product_category is not None:
                            category_encoded = product_category.encode('utf-8')
                        else:
                            category_encoded = product[2]

                        quantity = product_quantity if product_quantity is not None else product[3]
                        price = product_price if product_price is not None else product[4]

                        # เขียนข้อมูลสินค้าที่อัปเดตลงในไฟล์ชั่วคราว
                        data = struct.pack(PRODUCT_FORMAT,
                                        product_id,
                                        name_encoded,
                                        category_encoded,
                                        quantity,
                                        price)
                        temp_file.write(data)
                    else:
                        temp_file.write(data)   # เขียนสินค้าที่ไม่ถูกอัปเดตไปยังไฟล์ชั่วคราว

            if product_found:
                os.replace(temp_file_path, self.file_path)
                print(f"Product ID {product_id} successfully updated!")
            else:
                os.remove(temp_file_path)  # ลบไฟล์ชั่วคราวถ้าไม่พบสินค้า
                print(f"Product ID {product_id} not found!")

        except FileNotFoundError:
            print("File not found!")
        except Exception as e:
            print(f"An error occurred while updating the product: {e}")
            
    def export_inventory_report(self, output_file_path):
        """ส่งออกข้อมูลไปยังไฟล์ .txt ตามหมวดหมู่"""
        try:
            with open(self.file_path, 'rb') as file:
                categories = {}
                
                # อ่านข้อมูลสินค้าทั้งหมดและจัดกลุ่มตามหมวดหมู่
                while True:
                    data = file.read(PRODUCT_SIZE)
                    if not data:
                        break
                    product = struct.unpack(PRODUCT_FORMAT, data)

                    # แปลงข้อมูลให้ถูกต้อง
                    id_value = product[0]
                    name_value = product[1].decode('utf-8').strip('\x00')
                    category_value = product[2].decode('utf-8').strip('\x00')
                    quantity_value = product[3]
                    price_value = product[4]

                    # จัดกลุ่มสินค้าเข้าตามหมวดหมู่
                    if category_value not in categories:
                        categories[category_value] = []
                    categories[category_value].append((id_value, name_value, quantity_value, price_value))

            # เขียนข้อมูลลงไฟล์
            with open(output_file_path, 'w') as output_file:
                output_file.write(f"Inventory Report:\n")
                output_file.write(f"Number of categories: {len(categories)}\n")
                output_file.write('-'*70 + '\n\n')

                for category, products in categories.items():
                    total_price = sum(product[2] * product[3] for product in products)  # คำนวณราคารวมของหมวดหมู่
                    output_file.write(f"Category: {category}\n")
                    output_file.write(f"Number of Products: {len(products)}\n")
                    headers = ['ID', 'Name', 'Quantity', 'Price(THB)']
                    output_file.write('-'*70 + '\n')
                    output_file.write(f"{headers[0]:<7} {headers[1]:<30} {headers[2]:<10} {headers[3]:<10} \n")
                    output_file.write('-'*70 + '\n')

                    for id_value, name_value, quantity_value, price_value in products:
                        output_file.write(f"{id_value:03}{'':<3}  {name_value:<30} {quantity_value:<10} {price_value:<10,.2f}\n")
                    output_file.write("-"*70 +"\n") 
                    output_file.write(f"Total Price : {total_price:,.2f} THB\n")  # แสดงราคารวมของหมวดหมู่
                    output_file.write("-"*70 +"\n\n") # เพื่อเว้นบรรทัดระหว่างหมวดหมู่

            print(f"\nData successfully exported to '{output_file_path}' ! \n")
            
            input("Press Enter to return to the main menu...")# รอให้ผู้ใช้กด Enter ก่อนที่จะกลับไปที่เมนู

        except FileNotFoundError:
            print("File not found!")
        except Exception as e:
            print(f"An error occurred during data export: {e}")