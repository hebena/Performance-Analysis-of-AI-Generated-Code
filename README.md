# Replication package for: Performance Analysis of AI-Generated Code: A Case Study of Copilot, CodeLlaMa, and DeepSeek-Coder Models

Structure of the project:

There are four folders in this project: 
- **Data**:
  
    The original datasets and the rules used for PMD.
    
- **Root causes**:
  
    The root causes identified by author1 and author2.
    
- **Result**:
  
    1. Copilot: 

        1. results_for_humaneval

            - CPU
            
                This folder includes the CPU utilization results from HumanEval
                
            - Execution-Time
            
                This folder includes the Execution time results from HumanEval
                
            - Memory
            
                This folder includes the Memory usage results from HumanEval

        2. results_for_mbpp
        
            The file structure is the same as humaneval.
    
    2. CodeLlama: 

        The file structure is the same as Copilot.

    3. DeepSeek-Coder: 

        The file structure is the same as Copilot.
    
- **Scripts**:
  
    1. scripts_for_humaneval
        - Compare the generated code and canonical code
          
            `compare_copilot.py`, `compare_copilot_before_fewshot_prompt.py` and `compare_copilot_after_fewshot_prompt.py` will get the number of scripts with significant performance regressions in the Copilot-generated code, the Copilot-generated code before few-shot prompt engineering, and the Copilot-generated code after few-shot prompt engineering. The scripts of CodeLlama and DeepSeek-Coder have a format similar to Copilot.
            
        - Get dynamic results 
          
            `cprofile.py`, `memory.py` and `cpu.py` will get the dynamic results for Execution time, Memory usage, and CPU utilization.
            
        - Preparation work
          
            `add_@profile.py` and `add_for_function.py` will do the preparation work for dynamic analysis.
    
    2. scripts_for_mbpp
    
        The file structure is the same as humaneval.