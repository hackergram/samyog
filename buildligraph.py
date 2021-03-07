liws3=gd.open("LinkedIn Contacts").worksheets()[2]
contacts_graphed=liws3.get_all_records()
contacts_graphed_keys=[x['Key'] for x in contacts_graphed]
connects=contacts_all

for connect in connects:
    try:
        nodes.update(connect)
    except Exception as e:
        print(e)



for node in contacts_graphed:
    try:
        p=nodes.get(node['Key'])
        q=node['Connections'].split(",")
        print(p,q)
        for link in q:
            edges.link("nodes/"+node['Key'],"nodes/"+link, {"story":"is linked in to"})
    except:
        print("Oops")




for node in nodes:
    if node['_key']!='in_arjunvenkatraman':
        try:
            edges.link(nodes.get(node['_key']),nodes.get("in_arjunvenkatraman"),{"story":"is linked in to"})
        except:
            print(node)
