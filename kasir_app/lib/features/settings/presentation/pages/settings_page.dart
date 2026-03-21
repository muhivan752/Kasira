import 'package:flutter/material.dart';
import 'package:lucide_icons/lucide_icons.dart';
import '../../../../core/theme/app_colors.dart';

class SettingsPage extends StatelessWidget {
  const SettingsPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: Column(
        children: [
          // Header
          Container(
            padding: const EdgeInsets.all(24),
            color: Colors.white,
            width: double.infinity,
            child: Text('Pengaturan', style: Theme.of(context).textTheme.headlineMedium),
          ),
          
          // Settings List
          Expanded(
            child: ListView(
              padding: const EdgeInsets.all(24),
              children: [
                _buildSectionTitle('Perangkat & Hardware'),
                _buildSettingTile(
                  icon: LucideIcons.printer,
                  title: 'Printer Bluetooth',
                  subtitle: 'Epson TM-T82X (Terhubung)',
                  onTap: () {},
                ),
                _buildSettingTile(
                  icon: LucideIcons.monitorSpeaker,
                  title: 'Layar Pelanggan (Customer Display)',
                  subtitle: 'Tidak Terhubung',
                  onTap: () {},
                ),
                
                const SizedBox(height: 32),
                _buildSectionTitle('Sistem & Data'),
                _buildSettingTile(
                  icon: LucideIcons.refreshCw,
                  title: 'Sinkronisasi Data Manual',
                  subtitle: 'Terakhir sinkron: 10 menit yang lalu',
                  onTap: () {},
                ),
                _buildSettingTile(
                  icon: LucideIcons.database,
                  title: 'Hapus Cache Aplikasi',
                  subtitle: 'Kosongkan memori sementara',
                  onTap: () {},
                ),
                
                const SizedBox(height: 32),
                _buildSectionTitle('Akun & Bantuan'),
                _buildSettingTile(
                  icon: LucideIcons.user,
                  title: 'Profil Kasir',
                  subtitle: 'Budi (Shift Pagi)',
                  onTap: () {},
                ),
                _buildSettingTile(
                  icon: LucideIcons.helpCircle,
                  title: 'Pusat Bantuan',
                  subtitle: 'Hubungi tim support Kasira',
                  onTap: () {},
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSectionTitle(String title) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16, left: 8),
      child: Text(
        title.toUpperCase(),
        style: const TextStyle(
          color: AppColors.textSecondary,
          fontWeight: 'bold',
          fontSize: 12,
          letterSpacing: 1.2,
        ),
      ),
    );
  }

  Widget _buildSettingTile({
    required IconData icon,
    required String title,
    required String subtitle,
    required VoidCallback onTap,
  }) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: ListTile(
        contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
        leading: Container(
          padding: const EdgeInsets.all(10),
          decoration: BoxDecoration(
            color: AppColors.surfaceVariant,
            borderRadius: BorderRadius.circular(8),
          ),
          child: Icon(icon, color: AppColors.textSecondary),
        ),
        title: Text(title, style: const TextStyle(fontWeight: FontWeight.bold)),
        subtitle: Text(subtitle, style: const TextStyle(color: AppColors.textSecondary)),
        trailing: const Icon(LucideIcons.chevronRight, color: AppColors.textTertiary),
        onTap: onTap,
      ),
    );
  }
}
