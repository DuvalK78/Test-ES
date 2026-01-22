import json
import re
from pathlib import Path

class HTMLTeamGenerator:
    def __init__(self, data_file="teams_data.json"):
        with open(data_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
    
    def update_team_page(self, team_code, html_file):
        """Met à jour une page HTML d'équipe avec les nouvelles données"""
        
        if team_code not in self.data:
            print(f"⚠️  Pas de données pour {team_code}")
            return False
        
        team_data = self.data[team_code]
        stats = team_data.get('stats', {})
        
        # Lire le fichier HTML existant
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
        except FileNotFoundError:
            print(f"❌ Fichier {html_file} non trouvé")
            return False
        
        # Mettre à jour les stats
        updates = {
            # Win Rate
            r'<div class="num">[\d.]+%</div>\s*<div class="label">Win Rate \(saison\)</div>':
                f'<div class="num">{stats.get("win_rate", "0%")}</div>\n            <div class="label">Win Rate (saison)</div>',
            
            # KD moyen
            r'<div class="num">[\d.]+</div>\s*<div class="label">KD moyen</div>':
                f'<div class="num">{stats.get("kd_ratio", "0.00")}</div>\n            <div class="label">KD moyen</div>',
            
            # GPR
            r'<div class="num">[\d.]+</div>\s*<div class="label">Gol Percent Rating</div>':
                f'<div class="num">{stats.get("gpr", "0.00")}</div>\n            <div class="label">Gol Percent Rating</div>',
            
            # W-L Record
            r'<div class="num">[\d]+-[\d]+</div>\s*<div class="label">W-L</div>':
                f'<div class="num">{stats.get("record", "0-0")}</div>\n            <div class="label">W-L</div>',
            
            # Total Games
            r'<div class="num">[\d]+</div>\s*<div class="label">Total Games Played</div>':
                f'<div class="num">{stats.get("total_games", "0")}</div>\n            <div class="label">Total Games Played</div>',
            
            # Power Ranking
            r'<div class="num">#[\d]+ [\d]+pts</div>\s*<div class="label">Power Ranking</div>':
                f'<div class="num">{stats.get("power_ranking", "#0 0pts")}</div>\n            <div class="label">Power Ranking</div>',
            
            # First Blood %
            r'<div class="bar" style="width:[\d]+%"></div></div>\s*<div style="width:36px;text-align:right;font-weight:700;color:var\(--muted\)">[\d]+%</div>\s*</div>\s*<div class="role-row">\s*<div class="role-name">First Tower':
                f'<div class="bar" style="width:{stats.get("first_blood", "0%")}"></div></div>\n            <div style="width:36px;text-align:right;font-weight:700;color:var(--muted)">{stats.get("first_blood", "0%")}</div>\n          </div>\n          <div class="role-row">\n            <div class="role-name">First Tower',
            
            # Date de mise à jour
            r'<small style="color:var\(--muted\)">Dernière mise à jour: [\d]{4}-[\d]{2}-[\d]{2}</small>':
                f'<small style="color:var(--muted)">Dernière mise à jour: {stats.get("updated", "2025-01-22")}</small>'
        }
        
        # Appliquer les mises à jour
        for pattern, replacement in updates.items():
            html_content = re.sub(pattern, replacement, html_content)
        
        # Sauvegarder le fichier mis à jour
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ {team_code} mis à jour: {html_file}")
        return True
    
    def update_all_teams(self, teams_dir="./"):
        """Met à jour toutes les pages d'équipes"""
        
        team_files = {
            "KC": "K_Corp.html",
            "T1": "T1.html",
            "G2": "G2_eSports.html",
            "FNC": "Fnatic.html",
            "GENG": "Gen_G.html",
            "BLG": "BLG.html",
            "JDG": "JDG.html",
            "HLE": "HLE.html",
            "DRX": "DRX.html",
            "GM8": "Gentle_Mates.html",
            "AL": "AL.html"
        }
        
        updated = 0
        for team_code, filename in team_files.items():
            file_path = Path(teams_dir) / filename
            if self.update_team_page(team_code, file_path):
                updated += 1
        
        print(f"\n🎉 {updated}/{len(team_files)} équipes mises à jour!")
        return updated

    def generate_update_log(self, output_file="update_log.md"):
        """Génère un fichier de log des mises à jour"""
        from datetime import datetime
        
        log_content = f"# Mise à jour des stats - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        
        for team_code, team_data in self.data.items():
            stats = team_data.get('stats', {})
            log_content += f"## {stats.get('team_name', team_code)}\n"
            log_content += f"- Win Rate: {stats.get('win_rate', 'N/A')}\n"
            log_content += f"- KD Ratio: {stats.get('kd_ratio', 'N/A')}\n"
            log_content += f"- Record: {stats.get('record', 'N/A')}\n"
            log_content += f"- Power Ranking: {stats.get('power_ranking', 'N/A')}\n\n"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(log_content)
        
        print(f"📝 Log généré: {output_file}")


# Utilisation
if __name__ == "__main__":
    generator = HTMLTeamGenerator("teams_data.json")
    
    # Mettre à jour toutes les pages
    generator.update_all_teams("./")
    
    # Générer le log
    generator.generate_update_log()generator.py
