import csv, os, sys, django, random

BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

CSV_PATH    = 'initial_data/'
LOREM       = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras at rhoncus leo, ut tincidunt elit. Mauris vitae magna libero. Aenean iaculis lectus sed felis semper elementum. Etiam semper venenatis ante euismod convallis. Aenean malesuada blandit accumsan. Duis suscipit sapien quis nulla rhoncus, in tincidunt tortor pharetra.'

from user.models    import User, AdminLevel, Gender
from product.models import Menu, Category, ProductImageUrl, ProductQuestion, ProductAnswer, Subcategory, Brand, Product, Color, Size, ColorSize
from feed.models    import Feed, Comment, ImageUrl

def insert_user():
    with open(CSV_PATH + 'admin_levels.csv', 'r') as csvfile:
        for row in csv.DictReader(csvfile):
            AdminLevel.objects.create(name=row['name'])

    with open(CSV_PATH + 'genders.csv', 'r') as csvfile:
        for row in csv.DictReader(csvfile):
            Gender.objects.create(name=row['name'])

    with open(CSV_PATH + 'users.csv', 'r') as csvfile:
        for row in csv.DictReader(csvfile):
            User.objects.create(user_name=row['user_name'], password=row['password'], nickname=row['nickname'], email=row['email'])

            if row['admin_level_id']:
                temp = User.objects.latest('id')
                temp.admin_level_id = row['admin_level_id']
                temp.save()

def insert_product():
    with open(CSV_PATH + 'menus.csv', 'r') as csvfile:
        for row in csv.DictReader(csvfile):
            Menu.objects.create(name=row['name'])

    with open(CSV_PATH + 'categories.csv', 'r') as csvfile:
        for row in csv.DictReader(csvfile):
            Category.objects.create(name=row['name'], menu_id=row['menu_id'])

    with open(CSV_PATH + 'subcategories.csv', 'r') as csvfile:
        for row in csv.DictReader(csvfile):
            Subcategory.objects.create(name=row['name'], category_id=row['category_id'])

    with open(CSV_PATH + 'brands.csv', 'r') as csvfile:
        for row in csv.DictReader(csvfile):
            Brand.objects.create(name=row['name'], delivery_fee_cap=row['delivery_fee_cap'])
    
    with open(CSV_PATH + 'products.csv', 'r') as csvfile:
        for row in csv.DictReader(csvfile):
            Product.objects.create(subcategory_id=row['subcategory_id'], brand_id=row['brand_id'], name=row['name'], price=row['price'], discount_rate=row['discount_rate'])

    with open(CSV_PATH + 'product_image_urls.csv', 'r') as csvfile:
        for row in csv.DictReader(csvfile):
            ProductImageUrl.objects.create(product_id=row['product_id'], image_url=row['image_url'])

            if row['is_main']:
                temp = ProductImageUrl.objects.latest('id')
                temp.is_main = row['is_main']
                temp.save()

    with open(CSV_PATH + 'product_questions.csv', 'r') as csvfile:
        for row in csv.DictReader(csvfile):
            ProductQuestion.objects.create(user_id=row['user_id'], product_id=row['product_id'], content=row['content'])

    with open(CSV_PATH + 'product_answers.csv', 'r') as csvfile:
        for row in csv.DictReader(csvfile):
            ProductAnswer.objects.create(user_id=row['user_id'], product_question_id=row['productquestion__id'], content=row['content'])

def insert_option():
    with open(CSV_PATH + 'colors.csv', 'r') as csvfile:
        for row in csv.DictReader(csvfile):
            Color.objects.create(name=row['name'])

    with open(CSV_PATH + 'sizes.csv', 'r') as csvfile:
        for row in csv.DictReader(csvfile):
            Size.objects.create(name=row['name'])

# def insert_combination():


def insert_feed():
    with open(CSV_PATH + 'feeds.csv', 'r') as csvfile:
        for row in csv.DictReader(csvfile):
            Feed.objects.create(product_id=row['product'], user_id=['user_id'], description=LOREM[random.randint(0, 200):random.randint(201, 320)], like_number=random.randint(0, 200))

            if row['tag_item_number']:
                temp = Feed.objects.latest('id')
                temp.tag_item_number = row['tag_item_number']
                temp.save()

    table_length = Feed.objects.all().count()
    for i in range(table_length * 3):
        Comment.objects.create(feed_id=random.randint(1, table_length), user_id=random.randint(1, 17), content=LOREM[random.randint(0,50):random.randint(51, 100)])

    with open(CSV_PATH + 'image_url.csv', 'r') as csvfile:
        csv_dict        = csv.DictReader(csvfile)
        csv_dict_length = len(csv_dict)
        for i in range(3):
            for row in csv_dict:
                ImageUrl.objects.create(feed_id=(i * csv_dict_length)+int(row['feed_id']), image_url=row['image_url'])

insert_user()
insert_product()
insert_option()
insert_feed()
