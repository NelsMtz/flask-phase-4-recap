from app import app
from models import *

with app.app_context():    
    db.session.query(User).delete()
    db.session.query(Post).delete()
    db.session.query(Group).delete()
    db.session.query(user_groups).delete()
    db.session.commit()
    
    # User.query.delete()
    # Post.query.delete()
    # Group.query.delete()
    # db.session.delete(user_groups)

    print("Seeding user data.............")


    u1 = User(username='user1', email='john@example.com')
    u2 = User(username='user2', email='jane@example.com')
    u3 = User(username='user3', email='jim@example.com')
    u4 = User(username='user4', email='jill@example.com')
    u5 = User(username='user5', email='jack@example.com')

    db.session.add_all([u1, u2, u3, u4, u5])
    db.session.commit()

    p1 = Post(title='First Post', description='This is the first post', user=u1)
    p2 = Post(title='Second Post', description='This is the second post', user=u2)
    p3 = Post(title='Third Post', description='This is the third post', user=u3)
    p4 = Post(title='Fourth Post', description='This is the fourth post', user=u4)
    p5 = Post(title='Fifth Post', description='This is the fifth post', user=u5)
    p6 = Post(title='Sixth Post', description='This is the sixth post', user=u1)
    p7 = Post(title='Seventh Post', description='This is the seventh post', user=u2)
    p8 = Post(title='Eighth Post', description='This is the eighth post', user=u3)
    p9 = Post(title='Ninth Post', description='This is the ninth post', user=u4)
    p10 = Post(title='Tenth Post', description='This is the tenth post', user=u5)

    db.session.add_all([p1, p2, p3, p4, p5, p6, p7, p8, p9, p10])
    db.session.commit()

    g1 = Group(name='Group 1')
    g2 = Group(name='Group 2')
    g3 = Group(name='Group 3')
    g4 = Group(name='Group 4')
    g5 = Group(name='Group 5')

    db.session.add_all([g1, g2, g3, g4, g5])
    db.session.commit()


    # All groups to users
    u1.groups.append(g5)
    u1.groups.append(g2)

    # Add users to groups
    g5.users.append(u2)
    g5.users.append(u5)

    g4.users.append(u3)
    g4.users.append(u1)
     
    db.session.commit()
    print("Seeding complete")
