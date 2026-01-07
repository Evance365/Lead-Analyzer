from lead_analyzer import LeadAnalyzer
import os
import sys

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print application header"""
    print("\n" + "="*60)
    print(" " * 15 + " LEAD ANALYZER ")
    print(" " * 10 + "Data-Driven Lead Intelligence")
    print("="*60)

def print_menu():
    """Display the main menu"""
    print("\n" + "─"*60)
    print("  MAIN MENU")
    print("─"*60)
    print("  1.  Load CSV file")
    print("  2.  Clean data")
    print("  3.  Calculate conversion rate")
    print("  4.  Analyze by source")
    print("  5.  Analyze by status")
    print("  6.  Analyze trends (daily/weekly)")
    print("  7.  Create visualizations")
    print("  8.  Export report (CSV)")
    print("  9.  Export report (Excel)")
    print(" 10. ℹ  Show data info")
    print("  0.  Exit")
    print("─"*60)

def show_data_info(analyzer):
    """Display information about loaded data"""
    if analyzer is None or analyzer.df is None:
        print("\n⚠️  No data loaded yet")
        return
    
    print("\n" + "="*60)
    print("  DATA INFORMATION")
    print("="*60)
    
    df = analyzer.clean_df if analyzer.clean_df is not None else analyzer.df
    
    print(f"\nFile: {analyzer.csv_file}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"\nColumn Names:")
    for col in df.columns:
        print(f"  • {col} ({df[col].dtype})")
    
    print(f"\nFirst 5 rows preview:")
    print(df.head().to_string())
    print("="*60)

def main():
    analyzer = None
    
    # Clear screen and show header
    clear_screen()
    print_header()
    print("\n👋 Welcome! Let's analyze your lead data.\n")
    
    while True:
        print_menu()
        choice = input("\n👉 Enter your choice (0-10): ").strip()
        
        if choice == '1':
            print("\n" + "─"*60)
            file_path = input("📁 Enter CSV file path (or press Enter for '../data/sample_leads.csv'): ").strip()
            
            # Default to sample file if no input
            if not file_path:
                file_path = os.path.join('..', 'data', 'sample_leads.csv')
                print(f"   Using default: {file_path}")
            
            analyzer = LeadAnalyzer(file_path)
            if not analyzer.load_data():
                analyzer = None
                input("\nPress Enter to continue...")
            else:
                input("\nPress Enter to continue...")
                
        elif choice == '2':
            if analyzer is None or analyzer.df is None:
                print("\n⚠️  Please load a CSV file first (option 1)")
                input("Press Enter to continue...")
            else:
                analyzer.clean_data()
                input("\nPress Enter to continue...")
                
        elif choice == '3':
            if analyzer is None or analyzer.clean_df is None:
                print("\n⚠️  Please clean data first (option 2)")
                input("Press Enter to continue...")
            else:
                analyzer.calculate_conversion_rate()
                input("\nPress Enter to continue...")
                
        elif choice == '4':
            if analyzer is None or analyzer.clean_df is None:
                print("\n⚠️  Please clean data first (option 2)")
                input("Press Enter to continue...")
            else:
                analyzer.analyze_by_source()
                input("\nPress Enter to continue...")
                
        elif choice == '5':
            if analyzer is None or analyzer.clean_df is None:
                print("\n⚠️  Please clean data first (option 2)")
                input("Press Enter to continue...")
            else:
                analyzer.analyze_by_status()
                input("\nPress Enter to continue...")
                
        elif choice == '6':
            if analyzer is None or analyzer.clean_df is None:
                print("\n⚠️  Please clean data first (option 2)")
                input("Press Enter to continue...")
            else:
                analyzer.analyze_trends()
                input("\nPress Enter to continue...")
                
        elif choice == '7':
            if analyzer is None or analyzer.clean_df is None:
                print("\n⚠️  Please clean data first (option 2)")
                input("Press Enter to continue...")
            else:
                analyzer.create_visualizations()
                input("\nPress Enter to continue...")
                
        elif choice == '8':
            if analyzer is None or analyzer.clean_df is None:
                print("\n⚠️  Please clean data first (option 2)")
                input("Press Enter to continue...")
            else:
                analyzer.export_report('csv')
                input("\nPress Enter to continue...")
                
        elif choice == '9':
            if analyzer is None or analyzer.clean_df is None:
                print("\n⚠️  Please clean data first (option 2)")
                input("Press Enter to continue...")
            else:
                analyzer.export_report('excel')
                input("\nPress Enter to continue...")
                
        elif choice == '10':
            show_data_info(analyzer)
            input("\nPress Enter to continue...")
            
        elif choice == '0':
            print("\n" + "="*60)
            print("\n   Thanks for using Lead Analyzer!")
            print("   Don't forget to check your exported reports!\n")
            print("="*60 + "\n")
            break
            
        else:
            print("\n Invalid choice. Please enter a number from 0-10.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n Program interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n An unexpected error occurred: {e}")
        input("Press Enter to exit...")
        sys.exit(1)