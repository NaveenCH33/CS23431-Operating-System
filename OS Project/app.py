from flask import Flask, render_template, request, jsonify
from collections import deque
from datetime import datetime
import statistics

app = Flask(__name__)

def fifo_replacement(frames, pages):
    memory = deque(maxlen=frames)
    page_faults = 0
    steps = []
    
    for i, page in enumerate(pages):
        is_hit = page in memory
        old_state = list(memory)
        
        if not is_hit:
            page_faults += 1
            if len(memory) == frames:
                memory.popleft()  # Remove the first-in page
            memory.append(page)
        
        steps.append({
            'step': i + 1,
            'page': page,
            'memory_state': list(memory),
            'is_hit': is_hit,
            'page_faults': page_faults
        })
    
    return steps

def lru_replacement(frames, pages):
    memory = []
    page_faults = 0
    steps = []
    page_last_used = {}
    
    for i, page in enumerate(pages):
        is_hit = page in memory
        old_state = list(memory)
        
        if not is_hit:
            page_faults += 1
            if len(memory) == frames:
                # Find least recently used page
                lru_page = min(memory, key=lambda x: page_last_used[x])
                memory.remove(lru_page)
            memory.append(page)
        
        # Update last used time for current page
        page_last_used[page] = i
        
        steps.append({
            'step': i + 1,
            'page': page,
            'memory_state': list(memory),
            'is_hit': is_hit,
            'page_faults': page_faults
        })
    
    return steps

def optimal_replacement(frames, pages):
    memory = []
    page_faults = 0
    steps = []
    
    for i, page in enumerate(pages):
        is_hit = page in memory
        old_state = list(memory)
        
        if not is_hit:
            page_faults += 1
            if len(memory) == frames:
                # Find the page that won't be used for the longest time
                future_use = {}
                for p in memory:
                    try:
                        next_use = next(j for j in range(i + 1, len(pages)) if pages[j] == p)
                        future_use[p] = next_use
                    except StopIteration:
                        future_use[p] = float('inf')  # Page won't be used again
                
                # Remove the page that won't be used for the longest time
                page_to_remove = max(memory, key=lambda x: future_use[x])
                memory.remove(page_to_remove)
            memory.append(page)
        
        steps.append({
            'step': i + 1,
            'page': page,
            'memory_state': list(memory),
            'is_hit': is_hit,
            'page_faults': page_faults
        })
    
    return steps

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.get_json()
    pages = [int(x.strip()) for x in data['pages'].split(',')]
    frames = int(data['frames'])
    
    # Run all three algorithms
    fifo_steps = fifo_replacement(frames, pages)
    lru_steps = lru_replacement(frames, pages)
    optimal_steps = optimal_replacement(frames, pages)
    
    # Get final page faults for each algorithm
    fifo_faults = fifo_steps[-1]['page_faults']
    lru_faults = lru_steps[-1]['page_faults']
    optimal_faults = optimal_steps[-1]['page_faults']
    
    # Calculate statistics
    all_faults = [fifo_faults, lru_faults, optimal_faults]
    avg_faults = statistics.mean(all_faults)
    best_algorithm = min(
        [("FIFO", fifo_faults), ("LRU", lru_faults), ("Optimal", optimal_faults)],
        key=lambda x: x[1]
    )
    worst_algorithm = max(
        [("FIFO", fifo_faults), ("LRU", lru_faults), ("Optimal", optimal_faults)],
        key=lambda x: x[1]
    )
    
    # Calculate hit rates
    total_pages = len(pages)
    fifo_hit_rate = ((total_pages - fifo_faults) / total_pages) * 100
    lru_hit_rate = ((total_pages - lru_faults) / total_pages) * 100
    optimal_hit_rate = ((total_pages - optimal_faults) / total_pages) * 100
    
    return jsonify({
        'algorithms': {
            'fifo': {
                'steps': fifo_steps,
                'page_faults': fifo_faults,
                'hit_rate': round(fifo_hit_rate, 2)
            },
            'lru': {
                'steps': lru_steps,
                'page_faults': lru_faults,
                'hit_rate': round(lru_hit_rate, 2)
            },
            'optimal': {
                'steps': optimal_steps,
                'page_faults': optimal_faults,
                'hit_rate': round(optimal_hit_rate, 2)
            }
        },
        'statistics': {
            'average_faults': round(avg_faults, 2),
            'best_algorithm': {
                'name': best_algorithm[0],
                'faults': best_algorithm[1]
            },
            'worst_algorithm': {
                'name': worst_algorithm[0],
                'faults': worst_algorithm[1]
            }
        }
    })

if __name__ == '__main__':
    app.run(debug=True)
