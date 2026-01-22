import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

class LoLStatsScraper:
    def __init__(self):
        self.teams = {
            "KC": {"name": "Karmine Corp", "gol_id": "karmine-corp", "region": "LEC"},
            "T1": {"name": "T1", "gol_id": "t1", "region": "LCK"},
            "G2": {"name": "G2 Esports", "gol_id": "g2-esports", "region": "LEC"},
            "FNC": {"name": "Fnatic", "gol_id": "fnatic", "region": "LEC"},
            "GENG": {"name": "Gen.G", "gol_id": "gen-g", "region": "LCK"},
            "BLG": {"name": "Bilibili Gaming", "gol_id": "bilibili-gaming", "region": "LPL"},
            "JDG": {"name": "JD Gaming", "gol_id": "jd-gaming", "region": "LPL"},
            "HLE": {"name": "Hanwha Life Esports", "gol_id": "hanwha-life-esports", "region": "LCK"},
            "DRX": {"name": "DRX", "gol_id": "drx", "region": "LCK"},
            "GM8": {"name": "Gentle Mates", "gol_id": "gentle-mates", "region": "LEC"},
            "AL": {"name": "Aurora Lions", "gol_id": "aurora-lions", "region": "LEC"}
        }
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_gol_team_stats(self, team_code):
        """Scrape les stats d'une équipe depuis gol.gg"""
        team_info = self.teams.get(team_code)
        if not team_info:
            return None
        
        url = f"https://gol.gg/teams/team-stats/{team_info['gol_id']}/split-ALL/tournament-ALL/"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            stats = {
                "team_code": team_code,
                "team_name": team_info["name"],
                "region": team_info["region"],
                "updated": datetime.now().strftime("%Y-%m-%d"),
                "win_rate": "0%",
                "kd_ratio": "0.00",
                "gpr": "0.00",
                "tournaments_won": 0,
                "record": "0-0",
                "total_games": 0,
                "power_ranking": "#0 0pts",
                "first_blood": "0%",
                "first_tower": "0%",
                "first_dragon": "0%",
                "first_3_towers": "0%"
            }
            
            # Extraction des stats (à adapter selon la structure HTML de gol.gg)
            # Exemple de parsing - vous devrez l'ajuster selon le HTML réel
            stat_tables = soup.find_all('table', class_='table_list')
            
            for table in stat_tables:
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) >= 2:
                        label = cells[0].text.strip().lower()
                        value = cells[1].text.strip()
                        
                        if 'win rate' in label or 'winrate' in label:
                            stats['win_rate'] = value
                        elif 'k/d' in label or 'kd ratio' in label:
                            stats['kd_ratio'] = value
                        elif 'first blood' in label:
                            stats['first_blood'] = value
                        elif 'first tower' in label:
                            stats['first_tower'] = value
                        elif 'first dragon' in label:
                            stats['first_dragon'] = value
            
            return stats
            
        except Exception as e:
            print(f"Erreur lors du scraping de {team_code}: {e}")
            return None
    
    def scrape_team_roster(self, team_code):
        """Scrape le roster d'une équipe"""
        team_info = self.teams.get(team_code)
        if not team_info:
            return None
        
        url = f"https://gol.gg/teams/team-stats/{team_info['gol_id']}/split-ALL/tournament-ALL/"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            roster = []
            
            # Parser le roster (à adapter selon la structure HTML)
            player_sections = soup.find_all('div', class_='player-card') or soup.find_all('tr', class_='player-row')
            
            for player in player_sections:
                player_data = {
                    "name": "",
                    "role": "",
                    "kda": "0.0"
                }
                
                # Extraction des données joueur (à adapter)
                name_elem = player.find('span', class_='player-name') or player.find('a')
                if name_elem:
                    player_data['name'] = name_elem.text.strip()
                
                roster.append(player_data)
            
            return roster
            
        except Exception as e:
            print(f"Erreur lors du scraping du roster {team_code}: {e}")
            return None
    
    def scrape_all_teams(self):
        """Scrape toutes les équipes"""
        all_data = {}
        
        for team_code in self.teams.keys():
            print(f"Scraping {team_code}...")
            
            stats = self.scrape_gol_team_stats(team_code)
            roster = self.scrape_team_roster(team_code)
            
            all_data[team_code] = {
                "stats": stats,
                "roster": roster
            }
        
        return all_data
    
    def save_to_json(self, data, filename="teams_data.json"):
        """Sauvegarde les données en JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Données sauvegardées dans {filename}")


# Utilisation
if __name__ == "__main__":
    scraper = LoLStatsScraper()
    
    # Scraper toutes les équipes
    data = scraper.scrape_all_teams()
    
    # Sauvegarder
    scraper.save_to_json(data)
    
    print("\n✅ Scraping terminé!")
