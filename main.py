from function_inventory import *

def main():
    running = True
    inventory = Inventory('inventory.bin')

    while running:
        print('\nMenu')
        print('1. Display Product')
        print('2. Add Product')
        print('3. Update Product')
        print('4. Delete Product')
        print('5. Display Category Product')
        print('6. Export Inventory Report')
        print('7. Exit')

        try:
            menu = int(input('Enter your menu choice: '))
        
            if menu == 1:
                inventory.display_products()

            elif menu == 2:
                print('Add Product')
                while True:
                    try:
                        product_id = int(input('Enter Product ID: '))
                        # ตรวจสอบว่ารหัสสินค้าซ้ำหรือไม่
                        if inventory._check_product_exists(product_id):
                            print(f"Product ID {product_id} already exists. Please enter a different ID.")
                            continue  # ถ้าซ้ำ ให้เริ่มลูปใหม่
                        break  # ออกจากลูปหากไม่มีรหัสซ้ำ
                    except ValueError:
                        print("Invalid input. Please enter a valid integer for Product ID.")

                # รับข้อมูลสินค้าอื่น ๆ
                while True:
                    try:
                        product_name = input('Enter Product Name: ')
                        product_category = input('Enter Product Category: ')
                        product_quantity = int(input('Enter Product Quantity: '))
                        product_price = float(input('Enter Product Price: '))
                        inventory.add_product(product_id, product_name, product_category, product_quantity, product_price)
                        break  # ออกจากลูปถ้าข้อมูลถูกต้อง
                    except ValueError:
                        print("Invalid input. Please enter a valid number for Quantity and Price.")

            elif menu == 3:
                print('Update Product')
                inventory.display_products()  # แสดงรายการสินค้าก่อนเพื่อให้ผู้ใช้เลือก

                while True:
                    try:
                        product_id = int(input('Enter Product ID to update: '))
                        # เช็คว่ามี Product ID อยู่ในระบบหรือไม่
                        if not inventory._check_product_exists(product_id):
                            print(f"Product ID {product_id} does not exist. Please enter a valid ID.")
                            continue  # ถ้าไม่พบ ให้เริ่มลูปใหม่

                        # รับข้อมูลใหม่
                        product_name = input('Enter new Product Name (leave blank to keep current): ')
                        product_category = input('Enter new Product Category (leave blank to keep current): ')
                        product_quantity = input('Enter new Product Quantity (leave blank to keep current): ')
                        product_price = input('Enter new Product Price (leave blank to keep current): ')

                        # แปลงข้อมูลที่กรอกใหม่ให้เป็นชนิดที่ถูกต้อง
                        product_quantity = int(product_quantity) if product_quantity else None
                        product_price = float(product_price) if product_price else None

                        # เรียกใช้ฟังก์ชันอัปเดต
                        inventory.update_product(product_id, 
                                                product_name if product_name else None, 
                                                product_category if product_category else None, 
                                                product_quantity, 
                                                product_price)

                        break  # ออกจากลูปถ้าลบสำเร็จ
                    except ValueError:
                        print("Invalid input. Please enter valid numbers for Quantity and Price.")

            elif menu == 4:
                print('Delete Product')
                inventory.display_products()
                while True:
                    try:
                        product_id = int(input('Enter Product ID to delete: ')) # เช็คว่ามี Product ID อยู่ในระบบหรือไม่

                        if not inventory._check_product_exists(product_id):
                            print(f"Product ID {product_id} does not exist. Please enter a valid ID.")
                            continue  # ถ้าไม่พบ ให้เริ่มลูปใหม่

                        # ถ้าพบให้ลบ
                        inventory.delete_product(product_id)
                        break  # ออกจากลูปถ้าลบสำเร็จ
                    except ValueError:
                        print("Invalid input. Please enter a valid integer for Product ID.")

            elif menu == 5:   # เมนูสำหรับแสดงสินค้าตามหมวดหมู่
                inventory.generate_inventory_report()

            elif menu == 6:   # เมนูสำหรับสร้างรายงาน
                inventory.export_inventory_report('inventory_report.txt')

            elif menu == 7:   # เมนูหยุดทำงาน
                print('Exiting the program.')
                running = False
                
            else:
                print('Invalid Menu choice. Please try again.')
                
        except Exception as e:
            print(f"An error occurred: {e}")

main()

