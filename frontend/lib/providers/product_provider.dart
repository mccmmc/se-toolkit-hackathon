import 'package:flutter/material.dart';
import '../models/product.dart';
import '../services/api_service.dart';

class ProductProvider with ChangeNotifier {
  List<Product> _products = [];
  bool _isLoading = false;
  String? _error;

  List<Product> get products => _products;
  bool get isLoading => _isLoading;
  String? get error => _error;

  Future<void> loadProducts() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _products = await ApiService.getProducts();
      _error = null;
    } catch (e) {
      _error = 'Failed to load products: $e';
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> addProduct(String name, int quantity, int threshold) async {
    try {
      final product = await ApiService.createProduct(
        name: name,
        quantity: quantity,
        threshold: threshold,
      );
      _products.add(product);
      notifyListeners();
    } catch (e) {
      _error = 'Failed to add product: $e';
      notifyListeners();
    }
  }

  Future<void> updateQuantity(int productId, int newQuantity) async {
    if (newQuantity < 0) return;

    try {
      final product = await ApiService.updateQuantity(productId, newQuantity);
      final index = _products.indexWhere((p) => p.id == productId);
      if (index != -1) {
        _products[index] = product;
        notifyListeners();
      }
    } catch (e) {
      _error = 'Failed to update product: $e';
      notifyListeners();
    }
  }

  Future<void> deleteProduct(int productId) async {
    try {
      await ApiService.deleteProduct(productId);
      _products.removeWhere((p) => p.id == productId);
      notifyListeners();
    } catch (e) {
      _error = 'Failed to delete product: $e';
      notifyListeners();
    }
  }
}
