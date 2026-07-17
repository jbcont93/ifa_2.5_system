import 'package:flutter/material.dart';

/// Tema visual do IFA PRO 2.5 — paleta escura, tons de verde/azul para
/// remeter a analise de dados esportivos.
class IfaTheme {
  static ThemeData get dark {
    return ThemeData(
      brightness: Brightness.dark,
      useMaterial3: true,
      colorSchemeSeed: const Color(0xFF12B76A),
      scaffoldBackgroundColor: const Color(0xFF0B0F14),
      cardTheme: CardThemeData(
        color: const Color(0xFF141B22),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
      ),
      appBarTheme: const AppBarTheme(backgroundColor: Color(0xFF0B0F14), elevation: 0),
    );
  }

  static Color corClassificacao(String classificacao) {
    switch (classificacao) {
      case 'Elite':
        return const Color(0xFF12B76A);
      case 'Forte':
        return const Color(0xFFF79009);
      default:
        return const Color(0xFF667085);
    }
  }
}
