import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

/// Cliente HTTP central do app. Aponta para a API FastAPI do IFA PRO 2.5.
/// Troque [baseUrl] pelo endereco real do backend em producao.
class ApiClient {
  ApiClient({this.baseUrl = 'http://10.0.2.2:8000/api/v1'});

  final String baseUrl;
  final _storage = const FlutterSecureStorage();

  Future<String?> _token() => _storage.read(key: 'access_token');

  Future<Map<String, String>> _headers() async {
    final token = await _token();
    return {
      'Content-Type': 'application/json',
      if (token != null) 'Authorization': 'Bearer $token',
    };
  }

  Future<void> login(String email, String senha) async {
    final resp = await http.post(
      Uri.parse('$baseUrl/auth/login'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'email': email, 'senha': senha}),
    );
    if (resp.statusCode != 200) {
      throw Exception('Falha no login: ${resp.body}');
    }
    final data = jsonDecode(resp.body);
    await _storage.write(key: 'access_token', value: data['access_token']);
  }

  Future<void> logout() => _storage.delete(key: 'access_token');

  Future<Map<String, dynamic>> resumoDashboard() async {
    final resp = await http.get(Uri.parse('$baseUrl/dashboard/resumo'), headers: await _headers());
    _throwIfError(resp);
    return jsonDecode(resp.body) as Map<String, dynamic>;
  }

  Future<List<dynamic>> listarEliteEForte() async {
    final resp = await http.get(Uri.parse('$baseUrl/analises/elite-forte'), headers: await _headers());
    _throwIfError(resp);
    return jsonDecode(resp.body) as List<dynamic>;
  }

  Future<Map<String, dynamic>> obterRelatorio(int idPartida) async {
    final resp = await http.get(Uri.parse('$baseUrl/analises/relatorio/$idPartida'), headers: await _headers());
    _throwIfError(resp);
    return jsonDecode(resp.body) as Map<String, dynamic>;
  }

  void _throwIfError(http.Response resp) {
    if (resp.statusCode >= 400) {
      throw Exception('Erro ${resp.statusCode}: ${resp.body}');
    }
  }
}
