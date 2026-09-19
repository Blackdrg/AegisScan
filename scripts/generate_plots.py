import os
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def generate_plots():
    out_dir = Path("results/final_acceptance/plots")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Setup matplotlib defaults
    plt.style.use('default')
    plt.rcParams['figure.figsize'] = (8, 6)
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.alpha'] = 0.5
    plt.rcParams['lines.linewidth'] = 2
    plt.rcParams['font.size'] = 12

    # Load Scenario metrics
    scenario_csv = Path("results/final_acceptance/scenario_metrics.csv")
    if scenario_csv.exists():
        df_scen = pd.read_csv(scenario_csv)
        
        # 1. Pd vs SNR (from Scenario E)
        snr_scenarios = df_scen[df_scen['scenario'].str.contains('Scenario E')]
        if not snr_scenarios.empty:
            # Extract SNR values
            snr_scenarios = snr_scenarios.copy()
            snr_scenarios['SNR'] = snr_scenarios['scenario'].apply(lambda x: int(x.split('-')[-1].replace('dB','').strip()))
            snr_scenarios = snr_scenarios.sort_values('SNR')
            
            plt.figure()
            snr_scenarios['Pd'] = pd.to_numeric(snr_scenarios['Pd'], errors='coerce').fillna(0)
            plt.plot(snr_scenarios['SNR'], snr_scenarios['Pd'], marker='o')
            plt.title("Probability of Detection (Pd) vs SNR")
            plt.xlabel("SNR (dB)")
            plt.ylabel("Pd")
            plt.ylim(-0.1, 1.1)
            plt.savefig(out_dir / "pd_vs_snr.png", bbox_inches='tight', dpi=150)
            plt.close()
            
        # 2. Pfa by Scenario
        plt.figure(figsize=(10, 6))
        df_scen['Pfa'] = pd.to_numeric(df_scen['Pfa'], errors='coerce').fillna(0)
        plt.bar(df_scen['scenario'].apply(lambda x: x.split('-')[0].strip()), df_scen['Pfa'])
        plt.title("Probability of False Alarm (Pfa) by Scenario")
        plt.xlabel("Scenario")
        plt.ylabel("Pfa")
        plt.xticks(rotation=45, ha='right')
        plt.ylim(0, max(0.2, df_scen['Pfa'].max() * 1.2))
        plt.savefig(out_dir / "pfa_by_scenario.png", bbox_inches='tight', dpi=150)
        plt.close()

        # 3. Precision/Recall by Scenario
        plt.figure(figsize=(10, 6))
        scen_labels = df_scen['scenario'].apply(lambda x: x.split('-')[0].strip())
        x = range(len(df_scen))
        width = 0.35
        df_scen['Precision'] = pd.to_numeric(df_scen['Precision'], errors='coerce').fillna(0)
        df_scen['Recall'] = pd.to_numeric(df_scen['Recall'], errors='coerce').fillna(0)
        
        plt.bar([i - width/2 for i in x], df_scen['Precision'], width, label='Precision')
        plt.bar([i + width/2 for i in x], df_scen['Recall'], width, label='Recall')
        plt.title("Precision and Recall by Scenario")
        plt.xlabel("Scenario")
        plt.ylabel("Score")
        plt.xticks(x, scen_labels, rotation=45, ha='right')
        plt.legend()
        plt.ylim(0, 1.1)
        plt.savefig(out_dir / "precision_recall_by_scenario.png", bbox_inches='tight', dpi=150)
        plt.close()
        
    # Load Benchmark Summary
    benchmark_csv = Path("results/final_benchmark/aggregated/benchmark_summary.csv")
    if benchmark_csv.exists():
        df_bench = pd.read_csv(benchmark_csv)
        if not df_bench.empty:
            plt.figure(figsize=(10, 6))
            if 'Mean_Reward' in df_bench.columns:
                plt.bar(df_bench['Algorithm'], df_bench['Mean_Reward'])
                plt.title("Scheduler Mean Reward")
                plt.xlabel("Algorithm")
                plt.ylabel("Reward")
                plt.xticks(rotation=45, ha='right')
                plt.savefig(out_dir / "scheduler_actions.png", bbox_inches='tight', dpi=150)
                plt.close()
                
            plt.figure(figsize=(10, 6))
            if 'Mean_Coverage' in df_bench.columns:
                plt.bar(df_bench['Algorithm'], df_bench['Mean_Coverage'])
                plt.title("Scheduler Mean Coverage")
                plt.xlabel("Algorithm")
                plt.ylabel("Coverage")
                plt.xticks(rotation=45, ha='right')
                plt.savefig(out_dir / "scheduler_coverage.png", bbox_inches='tight', dpi=150)
                plt.close()
                
            # Copy to final acceptance
            import shutil
            shutil.copy(benchmark_csv, "results/final_acceptance/benchmark_summary.csv")

if __name__ == "__main__":
    generate_plots()
    print("Plots generated in results/final_acceptance/plots/")
