from Resources.Resource import load_resource

def main():
    load_resource()
    from BillingManagementSystem import starter as bms
    bms()

if __name__ == "__main__":
    main()
