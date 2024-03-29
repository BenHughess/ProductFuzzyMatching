import sys
import json

prod_f = open('')		# products file - txt
list_f = open('')		# listing file - txt
res_file = open('', 'w')	# result is written to this file - txt

result = {}
prod_dict = {}

# Get a { manufacturer: array[products] } dictionary
for line in prod_f:
    line = line.strip()
    pr = json.loads(line)
    try:
        prod_dict[pr["manufacturer"]].append(pr);
    except KeyError:
        l = []
        l.append(pr)
        prod_dict[pr["manufacturer"]] = l

# list of all manufacturers 
manu_list = list(prod_dict.keys())
    
cou = 0
co = 0	
for line in list_f:
    line = line.strip()
    item = json.loads(line)
    co = co + 1
    it1 = item['manufacturer'].replace(" ", "").replace("-", "").replace("_", "").lower()
    it2 = item['title'].replace(" ", "").replace("-", "").replace("_", "").lower()
    # Find the manufacturer of the item by looking at all the manufacturers
    for m in manu_list:
        # Remove spaces and convert to lowercase before pattern matching
        match_idx = it1.find(m.replace(" ", "").replace("-", "").replace("_", "").lower())
        if match_idx != -1:
            ma = 0
            p_name = ""
            # Find the matching item among all the items manufactured by that manufacturer
            for it in prod_dict[m]:
                # Remove spaces and convert to lowercase before pattern matching
                m_idx = it2.find(it['model'].replace(" ", "").replace("-", "").replace("_", "").lower()) 
                if m_idx != -1:
                    # Find the model name with maximum matching length
                    if len(it['model'].replace(" ", "").replace("-", "").replace("_", "")) > ma:
                        ma = len(it['model'].replace(" ", "").replace("-", "").replace("_", ""))
                        p_name = it['product_name']
            # If there is a product, add the item to the listing of that product
            if p_name != "":
                try:
                    result[p_name].append(item)
                    cou = cou + 1
                except KeyError:
                    l = []
                    l.append(item)
                    result[p_name] = l
                    cou = cou + 1

print("total listings : ",cou)
print("total number of matched listings : ", cou)

# convert the result to the required {'listing': array[item], 'product_name': string} format	
result_format = ({'product_name':k, 'listings':v} for (k, v) in result.items())
# write result to file
for item in result_format:
    res_file.write(str(json.dumps(item))+'\n')

res_file.close()
prod_f.close()
list_f.close()
