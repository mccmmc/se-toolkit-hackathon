import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/product.dart';
import '../providers/product_provider.dart';

class ProductCard extends StatelessWidget {
  final Product product;

  const ProductCard({super.key, required this.product});

  void _incrementQuantity(BuildContext context) {
    context.read<ProductProvider>().updateQuantity(product.id, product.quantity + 1);
  }

  void _decrementQuantity(BuildContext context) {
    if (product.quantity > 0) {
      context.read<ProductProvider>().updateQuantity(product.id, product.quantity - 1);
    }
  }

  void _confirmDelete(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Delete Product'),
        content: Text('Are you sure you want to delete "${product.name}"?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          TextButton(
            onPressed: () {
              context.read<ProductProvider>().deleteProduct(product.id);
              Navigator.pop(context);
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Text('${product.name} deleted'),
                  behavior: SnackBarBehavior.floating,
                ),
              );
            },
            child: const Text('Delete', style: TextStyle(color: Colors.red)),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final isLowStock = product.isLowStock;

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      elevation: isLowStock ? 4 : 2,
      color: isLowStock ? Colors.red[50] : null,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: isLowStock
            ? BorderSide(color: Colors.red[700]!, width: 2)
            : BorderSide.none,
      ),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Expanded(
                        child: Text(
                          product.name,
                          style: Theme.of(context).textTheme.titleLarge?.copyWith(
                            fontWeight: FontWeight.bold,
                            color: isLowStock ? Colors.red[900] : null,
                          ),
                        ),
                      ),
                      if (isLowStock)
                        Container(
                          padding: const EdgeInsets.symmetric(
                            horizontal: 8,
                            vertical: 4,
                          ),
                          decoration: BoxDecoration(
                            color: Colors.red[700],
                            borderRadius: BorderRadius.circular(12),
                          ),
                          child: const Text(
                            'LOW STOCK',
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 10,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  Row(
                    children: [
                      Text(
                        'Quantity: ${product.quantity}',
                        style: TextStyle(
                          fontSize: 16,
                          color: isLowStock ? Colors.red[700] : Colors.grey[700],
                          fontWeight: isLowStock ? FontWeight.bold : FontWeight.normal,
                        ),
                      ),
                      const SizedBox(width: 16),
                      Text(
                        'Threshold: ${product.threshold}',
                        style: TextStyle(
                          fontSize: 14,
                          color: Colors.grey[600],
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
            const SizedBox(width: 8),
            Column(
              children: [
                IconButton.filledTonal(
                  onPressed: () => _incrementQuantity(context),
                  icon: const Icon(Icons.add),
                  tooltip: 'Increase quantity',
                ),
                const SizedBox(height: 4),
                IconButton.filledTonal(
                  onPressed: () => _decrementQuantity(context),
                  icon: const Icon(Icons.remove),
                  tooltip: 'Decrease quantity',
                ),
                const SizedBox(height: 4),
                IconButton.outlined(
                  onPressed: () => _confirmDelete(context),
                  icon: const Icon(Icons.delete_outline, color: Colors.red),
                  tooltip: 'Delete product',
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
