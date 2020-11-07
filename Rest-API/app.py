from flask import Flask, jsonify, request
 
app = Flask(__name__)

from products import products

@app.route('/ping')
def ping():
    return jsonify({"mensaje": "pong!"})

@app.route('/products')
def getProducts():
    return jsonify({"productos" : products}) 

@app.route('/products/<string:productName>')
def getProduct(productName):
    productFound = [product for product in products if product['name'] == productName]
    if (len(productFound) > 0):
        return jsonify({"product" : productFound[0]}) 
    return jsonify({"message" : "Product not found"})

@app.route('/products', methods=['POST'])
def addProduct():    
    newProduct = {
        "name" : request.json['name'],
        "price" : request.json['price'],
        "quantity" : request.json['quantity']
    }
    products.append(newProduct)
    return jsonify({"message" : "Product Added Succesfully", "products" : products})

@app.route('/products/<string:productName>', methods=['PUT'])    
def editProduct(productName):
    productFound = [product for product in products if product['name'] == productName]
    if (len(productFound) > 0):
        productFound[0]['name'] = request.json['name']
        productFound[0]['price'] = request.json['price']
        productFound[0]['quantity'] = request.json['quantity']
        return jsonify({
            "message" : "Product update",
            "product" : productFound[0] 
        })
    return jsonify({"message" : "Product Not found"})


@app.route('/products/<string:productName>', methods=['DELETE']) 
def deleteProduct(productName):
    productFound = [product for product in products if product['name'] == productName]
    if (len(productFound) > 0):
        products.remove(productFound[0])
        return jsonify({
            "message" : "Product Deleted",
            "product" : products
        })
    return jsonify({"message" : "Product Not found"})

if __name__ == '__main__':
    app.run(debug=True, port=4000)