from flask import Flask, request, render_template, jsonify
import pandas as pd
import os
import time
import importlib.util
import re
import shutil

app = Flask(__name__)

def load_adapter(adapter_name):
    adapter_path = os.path.join("adapters", f"{adapter_name}.py")
    spec = importlib.util.spec_from_file_location(adapter_name, adapter_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def get_adapter_names():
    return [f.replace(".py", "") for f in os.listdir("adapters") if f.endswith(".py")]

@app.route('/')
def index():
    adapter_names = get_adapter_names()
    return render_template('index.html', adapter_names=adapter_names)

@app.route('/run_migration', methods=['POST'])
def run_migration():
    start_time = time.time()
    file = request.files['input_file']
    if not file:
        return jsonify({
            "status": "error",
            "message": "No file uploaded.",
            "debug": []
        })

    if not file.filename.lower().endswith('.csv'):
        return jsonify({
            "status": "error",
            "message": "Only CSV files are supported.",
            "debug": []
        })

    adapter_name = re.sub(r'\W+', '_', request.form.get("adapter_name")).lower()
    adapter_path = os.path.join("adapters", f"{adapter_name}.py")
    if not os.path.exists(adapter_path):
        return jsonify({
            "status": "error",
            "message": f"Adapter '{adapter_name}' not found.",
            "debug": []
        })

    try:
        temp_path = os.path.join("temp", file.filename)
        os.makedirs("temp", exist_ok=True)
        file.save(temp_path)
        file_directory = os.path.dirname(os.path.abspath(temp_path))

        df = pd.read_csv(temp_path)
        adapter = load_adapter(adapter_name)
        transformed_result = adapter.transform(selected_file=temp_path, file_directory=file_directory)

        # Call save_transformed only if it exists
        output_path = None
        if hasattr(adapter, "save_transformed"):
            output_path = adapter.save_transformed(transformed_result, adapter_name, temp_path)

        # Handle summary dictionary from adapter
        if isinstance(transformed_result, dict):
            success_count = transformed_result.get("written", 0)
            skipped_count = transformed_result.get("skipped", 0)
        elif isinstance(transformed_result, pd.DataFrame):
            success_count = len(transformed_result)
            skipped_count = 0
        else:
            raise ValueError("Adapter returned an unexpected result type.")

        # Safely format output path
        csv_path = "/" + output_path.replace("\\", "/") if output_path else "#"

        return jsonify({
            "status": "success",
            "summary": {
                "total": len(df),
                "success": success_count,
                "skipped": skipped_count,
                "duration": round(time.time() - start_time, 2),
                "errors": []
            },
            "report_paths": {
                "csv": csv_path,
                "xlsx": "#",
                "pdf": "#"
            },
            "debug": []
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "debug": [str(e)]
        })

    finally:
        try:
            temp_dir = os.path.join(os.path.dirname(__file__), "temp")
            if os.path.isdir(temp_dir):
                for f in os.listdir(temp_dir):
                    path = os.path.join(temp_dir, f)
                    if os.path.isfile(path):
                        os.remove(path)
                    elif os.path.isdir(path):
                        shutil.rmtree(path)
        except Exception as cleanup_error:
            print(f"⚠️ Cleanup failed: {cleanup_error}")
            
if __name__ == '__main__':
    app.run(debug=True)