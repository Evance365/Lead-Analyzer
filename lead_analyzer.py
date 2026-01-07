import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

class LeadAnalyzer:
    def __init__(self, csv_file):
        """Initialize with a CSV file path"""
        self.csv_file = csv_file
        self.df = None
        self.clean_df = None
        
    def load_data(self):
        """Load the CSV into a pandas DataFrame"""
        try:
            self.df = pd.read_csv(self.csv_file)
            print(f"✓ Loaded {len(self.df)} leads from {self.csv_file}")
            print(f"\nColumns found: {', '.join(self.df.columns.tolist())}")
            print(f"Shape: {self.df.shape[0]} rows × {self.df.shape[1]} columns")
            return True
        except FileNotFoundError:
            print(f"✗ Error: File '{self.csv_file}' not found")
            return False
        except Exception as e:
            print(f"✗ Error loading file: {e}")
            return False
    
    def clean_data(self):
        """Clean and standardize the data"""
        if self.df is None:
            print("Please load data first")
            return
            
        print("\n Cleaning data...")
        self.clean_df = self.df.copy()  # Work on a copy
        
        # 1. Handle missing values
        print(f"\n  Missing values before cleaning:")
        missing_before = self.clean_df.isnull().sum()
        print(missing_before[missing_before > 0])
        
        # Fill missing phone numbers with 'Not provided'
        self.clean_df['phone'].fillna('Not provided', inplace=True)
        
        # Fill missing emails with 'Not provided'
        self.clean_df['email'].fillna('Not provided', inplace=True)
        
        # Fill missing lead_value with 0
        self.clean_df['lead_value'].fillna(0, inplace=True)
        
        # 2. Standardize text fields (remove extra spaces, capitalize properly)
        self.clean_df['source'] = self.clean_df['source'].str.strip().str.title()
        self.clean_df['status'] = self.clean_df['status'].str.strip().str.title()
        self.clean_df['name'] = self.clean_df['name'].str.strip()
        
        # 3. Validate and clean emails
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        invalid_emails = ~self.clean_df['email'].str.match(email_pattern, na=False)
        invalid_count = invalid_emails.sum()
        self.clean_df.loc[invalid_emails, 'email'] = 'Invalid email'
        
        if invalid_count > 0:
            print(f"    Found and marked {invalid_count} invalid email(s)")
        
        # 4. Convert date column to datetime
        self.clean_df['date_added'] = pd.to_datetime(self.clean_df['date_added'])
        
        # 5. Ensure lead_value is numeric
        self.clean_df['lead_value'] = pd.to_numeric(self.clean_df['lead_value'], errors='coerce').fillna(0)
        
        print(f"\n✓ Data cleaned! {len(self.clean_df)} leads ready for analysis")
        print(f"  Missing values after cleaning: {self.clean_df.isnull().sum().sum()}")
        
    def calculate_conversion_rate(self):
        """Calculate overall conversion rate"""
        if self.clean_df is None:
            print("Please clean data first")
            return
        
        total = len(self.clean_df)
        converted = len(self.clean_df[self.clean_df['status'] == 'Converted'])
        rate = (converted / total) * 100 if total > 0 else 0
        
        print(f"\n CONVERSION RATE ANALYSIS")
        print("=" * 50)
        print(f"Total Leads: {total}")
        print(f"Converted Leads: {converted}")
        print(f"Conversion Rate: {rate:.2f}%")
        print("=" * 50)
        
        return rate
    
    def analyze_by_source(self):
        """Analyze performance by lead source"""
        if self.clean_df is None:
            print("Please clean data first")
            return
        
        print(f"\n PERFORMANCE BY LEAD SOURCE")
        print("=" * 80)
        
        source_stats = self.clean_df.groupby('source').agg({
            'lead_id': 'count',
            'lead_value': 'sum',
            'status': lambda x: (x == 'Converted').sum()
        }).rename(columns={
            'lead_id': 'total_leads',
            'lead_value': 'total_value',
            'status': 'conversions'
        })
        
        source_stats['conversion_rate'] = (
            source_stats['conversions'] / source_stats['total_leads'] * 100
        ).round(2)
        
        source_stats['avg_lead_value'] = (
            source_stats['total_value'] / source_stats['total_leads']
        ).round(2)
        
        # Sort by total value
        source_stats = source_stats.sort_values('total_value', ascending=False)
        
        print(source_stats.to_string())
        print("=" * 80)
        
        # Find best performing source
        best_source = source_stats['conversion_rate'].idxmax()
        best_rate = source_stats.loc[best_source, 'conversion_rate']
        print(f"\n Best Performing Source: {best_source} ({best_rate}% conversion rate)")
        
        return source_stats
    
    def analyze_by_status(self):
        """Analyze leads by status"""
        if self.clean_df is None:
            print("Please clean data first")
            return
        
        print(f"\n LEADS BY STATUS")
        print("=" * 50)
        
        status_counts = self.clean_df['status'].value_counts()
        status_percentages = (status_counts / len(self.clean_df) * 100).round(2)
        
        status_df = pd.DataFrame({
            'Count': status_counts,
            'Percentage': status_percentages
        })
        
        print(status_df.to_string())
        print("=" * 50)
        
        return status_df
    
    def analyze_trends(self):
        """Analyze daily/weekly trends"""
        if self.clean_df is None:
            print("Please clean data first")
            return
        
        print(f"\n DAILY TRENDS")
        print("=" * 70)
        
        daily = self.clean_df.groupby(
            self.clean_df['date_added'].dt.date
        ).agg({
            'lead_id': 'count',
            'lead_value': 'sum',
            'status': lambda x: (x == 'Converted').sum()
        }).rename(columns={
            'lead_id': 'leads_added',
            'lead_value': 'total_value',
            'status': 'conversions'
        })
        
        daily['conversion_rate'] = (
            daily['conversions'] / daily['leads_added'] * 100
        ).round(2)
        
        print(daily.to_string())
        print("=" * 70)
        
        # Calculate weekly trends
        print(f"\n WEEKLY TRENDS")
        print("=" * 70)
        
        weekly = self.clean_df.groupby(
            self.clean_df['date_added'].dt.to_period('W')
        ).agg({
            'lead_id': 'count',
            'lead_value': 'sum',
            'status': lambda x: (x == 'Converted').sum()
        }).rename(columns={
            'lead_id': 'leads_added',
            'lead_value': 'total_value',
            'status': 'conversions'
        })
        
        print(weekly.to_string())
        print("=" * 70)
        
        return daily, weekly
    
    def create_visualizations(self):
        """Generate charts for insights"""
        if self.clean_df is None:
            print("Please clean data first")
            return
        
        print("\n Creating visualizations...")
        
        # Create a figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Lead Analysis Dashboard', fontsize=16, fontweight='bold')
        
        # 1. Leads by Source
        source_counts = self.clean_df['source'].value_counts()
        colors_bar = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
        axes[0, 0].bar(source_counts.index, source_counts.values, color=colors_bar[:len(source_counts)])
        axes[0, 0].set_title('Leads by Source', fontsize=12, fontweight='bold')
        axes[0, 0].set_xlabel('Source')
        axes[0, 0].set_ylabel('Number of Leads')
        axes[0, 0].tick_params(axis='x', rotation=45)
        axes[0, 0].grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for i, v in enumerate(source_counts.values):
            axes[0, 0].text(i, v + 0.1, str(v), ha='center', va='bottom')
        
        # 2. Leads by Status (Pie Chart)
        status_counts = self.clean_df['status'].value_counts()
        colors_pie = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12']
        axes[0, 1].pie(status_counts.values, labels=status_counts.index, 
                       autopct='%1.1f%%', startangle=90, colors=colors_pie[:len(status_counts)])
        axes[0, 1].set_title('Leads by Status', fontsize=12, fontweight='bold')
        
        # 3. Lead Value by Source
        value_by_source = self.clean_df.groupby('source')['lead_value'].sum().sort_values()
        axes[1, 0].barh(value_by_source.index, value_by_source.values, color='#2ecc71')
        axes[1, 0].set_title('Total Lead Value by Source', fontsize=12, fontweight='bold')
        axes[1, 0].set_xlabel('Total Value ($)')
        axes[1, 0].grid(axis='x', alpha=0.3)
        
        # Add value labels
        for i, v in enumerate(value_by_source.values):
            axes[1, 0].text(v + 100, i, f'${v:,.0f}', va='center')
        
        # 4. Daily Lead Trends
        daily_counts = self.clean_df.groupby(
            self.clean_df['date_added'].dt.date
        ).size()
        axes[1, 1].plot(daily_counts.index, daily_counts.values, marker='o', 
                        color='#e74c3c', linewidth=2, markersize=6)
        axes[1, 1].fill_between(daily_counts.index, daily_counts.values, alpha=0.3, color='#e74c3c')
        axes[1, 1].set_title('Daily Lead Volume', fontsize=12, fontweight='bold')
        axes[1, 1].set_xlabel('Date')
        axes[1, 1].set_ylabel('Number of Leads')
        axes[1, 1].tick_params(axis='x', rotation=45)
        axes[1, 1].grid(alpha=0.3)
        
        plt.tight_layout()
        
        # Save the figure
        output_file = 'lead_analysis_charts.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✓ Charts saved to {output_file}")
        
        # Show the plot
        plt.show()
        
    def export_report(self, format='csv'):
        """Export cleaned data and summary report"""
        if self.clean_df is None:
            print("Please clean data first")
            return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        print(f"\n Exporting reports...")
        
        # Export cleaned data
        if format == 'csv':
            clean_file = f'cleaned_leads_{timestamp}.csv'
            self.clean_df.to_csv(clean_file, index=False)
            print(f"✓ Cleaned data exported to: {clean_file}")
        elif format == 'excel':
            clean_file = f'cleaned_leads_{timestamp}.xlsx'
            
            # Create Excel writer with multiple sheets
            with pd.ExcelWriter(clean_file, engine='openpyxl') as writer:
                # Sheet 1: Cleaned data
                self.clean_df.to_excel(writer, sheet_name='Cleaned Leads', index=False)
                
                # Sheet 2: Source analysis
                source_stats = self.clean_df.groupby('source').agg({
                    'lead_id': 'count',
                    'lead_value': 'sum',
                    'status': lambda x: (x == 'Converted').sum()
                }).rename(columns={
                    'lead_id': 'total_leads',
                    'lead_value': 'total_value',
                    'status': 'conversions'
                })
                source_stats['conversion_rate'] = (
                    source_stats['conversions'] / source_stats['total_leads'] * 100
                ).round(2)
                source_stats.to_excel(writer, sheet_name='Source Analysis')
                
                # Sheet 3: Status breakdown
                status_stats = self.clean_df['status'].value_counts().to_frame('count')
                status_stats['percentage'] = (status_stats['count'] / len(self.clean_df) * 100).round(2)
                status_stats.to_excel(writer, sheet_name='Status Breakdown')
            
            print(f"✓ Cleaned data exported to: {clean_file}")
            print(f"  (Contains 3 sheets: Cleaned Leads, Source Analysis, Status Breakdown)")
        
        # Create summary report
        summary_file = f'lead_summary_{timestamp}.txt'
        with open(summary_file, 'w') as f:
            f.write("=" * 70 + "\n")
            f.write(" " * 20 + "LEAD ANALYSIS SUMMARY REPORT\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Data Source: {self.csv_file}\n\n")
            
            f.write("OVERVIEW:\n")
            f.write("-" * 70 + "\n")
            f.write(f"Total Leads: {len(self.clean_df)}\n")
            f.write(f"Date Range: {self.clean_df['date_added'].min().date()} to "
                   f"{self.clean_df['date_added'].max().date()}\n")
            f.write(f"Total Lead Value: ${self.clean_df['lead_value'].sum():,.2f}\n")
            f.write(f"Average Lead Value: ${self.clean_df['lead_value'].mean():,.2f}\n\n")
            
            # Conversion rate
            total = len(self.clean_df)
            converted = len(self.clean_df[self.clean_df['status'] == 'Converted'])
            rate = (converted / total) * 100 if total > 0 else 0
            f.write(f"Conversion Rate: {rate:.2f}% ({converted} converted out of {total})\n\n")
            
            f.write("STATUS BREAKDOWN:\n")
            f.write("-" * 70 + "\n")
            status_str = self.clean_df['status'].value_counts().to_string()
            f.write(status_str)
            f.write("\n\n")
            
            f.write("SOURCE BREAKDOWN:\n")
            f.write("-" * 70 + "\n")
            source_str = self.clean_df['source'].value_counts().to_string()
            f.write(source_str)
            f.write("\n\n")
            
            # Top sources by value
            f.write("TOP SOURCES BY VALUE:\n")
            f.write("-" * 70 + "\n")
            top_sources = self.clean_df.groupby('source')['lead_value'].sum().sort_values(ascending=False)
            f.write(top_sources.to_string())
            f.write("\n\n")
            
            f.write("=" * 70 + "\n")
            f.write("End of Report\n")
            f.write("=" * 70 + "\n")
        
        print(f"✓ Summary report exported to: {summary_file}")
        print(f"\n Export complete! Generated {2 if format == 'csv' else 2} file(s)")
        
        
        