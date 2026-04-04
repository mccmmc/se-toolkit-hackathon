class Product {
  final int id;
  final String name;
  final int quantity;
  final int threshold;

  Product({
    required this.id,
    required this.name,
    required this.quantity,
    required this.threshold,
  });

  bool get isLowStock => quantity <= threshold;

  factory Product.fromJson(Map<String, dynamic> json) {
    return Product(
      id: json['id'],
      name: json['name'],
      quantity: json['quantity'],
      threshold: json['threshold'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'quantity': quantity,
      'threshold': threshold,
    };
  }
}
