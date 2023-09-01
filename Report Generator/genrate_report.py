import json
import pandas as pd
from jinja2 import Environment, FileSystemLoader
import matplotlib.pyplot as plt

COLORZ = ['#F5F5F5', '#555555', '#808080', '#AAAAAA', '#D3D3D3', 
              '#E5E4E2', '#999999', '#999966', '#777777', '#DCDCDC']

RISK_COLORS = {'Critical': '#980000', 'High': '#ff0000', 'Medium': '#ff9900', 'Low': '#ffff00', 'Very Low': '#00ff00'}

# --------functions------------

# This function is used for specific scenarios, not needed for most cases
def count_and_plot_unique_prefixes(filtered_data, output_file):
    # Use regular expression to extract the prefix from each unique row
    unique_prefixes = filtered_data[['meta_usecases.threats.name', 'meta_name','meta_usecases.threats.risk']].drop_duplicates()
    unique_prefixes = unique_prefixes['meta_usecases.threats.name']
    unique_prefixes = pd.Series(unique_prefixes).str.extract('^(\(.*?\))', expand=False)

    unique_prefixes = unique_prefixes.str.replace('\(W\)', 'Widgets', regex=True)
    unique_prefixes = unique_prefixes.str.replace('\(G \+ W\)', 'General and Widgets', regex=True)
    unique_prefixes = unique_prefixes.str.replace('\(G\)', 'General', regex=True)

    # Count the number of rows with each prefix
    counts = unique_prefixes.value_counts()
    
    fig, ax = plt.subplots()
    ax.pie(counts.values, colors=COLORZ, labels=counts.index, autopct=lambda x: '{:.0f}'.format(x*counts.values.sum()/100), shadow = True,startangle=90) 
    ax.set_title('Number of Threats by Type')
    
    # Save the plot to the specified file
    plt.savefig(output_file, dpi=150, bbox_inches='tight')

def count_and_plot_unique_components(filtered_data, output_file):
    unique_threats = filtered_data[['meta_usecases.threats.name', 'meta_name','meta_usecases.threats.risk']].drop_duplicates()
    
    counts = unique_threats['meta_name'].value_counts()
    
    fig, ax = plt.subplots()

    ax.pie(counts.values, colors=COLORZ, labels=counts.index, autopct=lambda x: '{:.0f}'.format(x*counts.values.sum()/100), shadow = True,startangle=0) 
    ax.set_title('Number of Threats by Component')

    # Save the plot to the specified file
    plt.savefig(output_file, dpi=150, bbox_inches='tight')

def count_and_plot_risks(filtered_data, output_file):
    unique_prefixes = filtered_data[['meta_usecases.threats.name', 'meta_name','meta_usecases.threats.risk']].drop_duplicates()
    
    counts = unique_prefixes['meta_usecases.threats.risk'].value_counts()
    
    counts = counts.loc[['Critical', 'High', 'Medium', 'Low', 'Very Low']]

    # Remove all values that are empty
    counts = counts[counts != 0]  
     
    # Set colors for the pie chart slices
    pie_colors = [RISK_COLORS.get(x, 'gray') for x in counts.index]

    # Plot the pie chart
    fig, ax = plt.subplots()
    ax.pie(counts.values, colors=pie_colors, labels=counts.index, autopct=lambda x: '{:.0f}'.format(x*counts.values.sum()/100), shadow=True, startangle=90)
    ax.set_title('Number of Threats by Risk Level')
    
    # Save the plot to the specified file
    plt.savefig(output_file, dpi=150, bbox_inches='tight')

def read_required_tags_from_config(config_file):
    try:
        with open(config_file, 'r') as f:
            config_data = json.load(f)
            required_tags = config_data.get('required_tags', [])
            if not isinstance(required_tags, list):
                print("Error: required_tags in the config file is not a list. Using an empty list instead.")
                required_tags = ['']
    except FileNotFoundError:
        print(f"Error: {config_file} not found. Using an empty list for required_tags.")
        required_tags = ['']
    except json.JSONDecodeError:
        print(f"Error: {config_file} contains invalid JSON. Using an empty list for required_tags.")
        required_tags = ['']
    
    return required_tags

def read_product_info(file_path):
    try:
        with open(file_path) as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: product_info.json not found.")
    except json.JSONDecodeError:
        print("Error: product_info.json contains invalid JSON.")
    return []

def filter_required_tags(tags, required_tags):
    return any(tag in required_tags for tag in tags)

# Prepares content of Threat Narratives
def generate_table_data(filtered_df):
    table_data = []
    grouped_data = filtered_df.groupby('meta_usecases.threats.name')
    #This code sorts the groups by the index of the risk value in the tuple if the risk value is in the tuple; otherwise, it assigns the index 999 to the group, which ensures that it will be placed at the end of the sorted list.
    sorted_groups = sorted(grouped_data, key=lambda x: ('Critical', 'High', 'Medium', 'Low', 'Very Low').index(x[1]['meta_usecases.threats.risk'].iloc[0]) if x[1]['meta_usecases.threats.risk'].iloc[0] in ('Critical', 'High', 'Medium', 'Low', 'Very Low') else 999)
    for name, group in sorted_groups:
        table = group[['meta_name', 'meta_usecases.threats.risk','meta_tags', '_name', '_state']].rename(columns={
            'meta_name': 'Impacted component',
            'meta_usecases.threats.risk': 'Risk for component',
            'meta_tags': 'Tags',
            '_name': 'Countermeasure Name',
            '_state': 'Countermeasure Status'
        })
        table['Tags'] = table['Tags'].apply(lambda tags: ' '.join(tags))
        table_data.append({
            'title': f"{group['meta_usecases.threats.risk'].iloc[0]} - {group['meta_usecases.threats.name'].iloc[0]} - {group['meta_usecases.threats.state'].iloc[0]}",
            'desc': group['meta_usecases.threats.desc'].iloc[0],
            'table': table
        })

    return table_data

def render_template_to_file(template_file, output_file, context):
    env = Environment(loader=FileSystemLoader('.'))
    env.globals['enumerate'] = enumerate
    template = env.get_template(template_file)

    with open(output_file, 'w') as f:
        html_content = template.render(**context)
        f.write(html_content)

def add_empty_string_to_tags(product_info):
    for component in product_info['components']:
        component['tags'].append('')

def process_countermeasures(countermeasures_df):
    countermeasures_df = countermeasures_df[['_name', '_desc', 'meta_name']].rename(columns={
        '_name': 'Countermeasure Name',
        '_desc': 'Countermeasure Description',
        'meta_name': 'Impacted component'
    })

    countermeasures_grouped = countermeasures_df.groupby('Countermeasure Name').agg({
        'Countermeasure Description': 'first',
        'Impacted component': lambda x: ', '.join(set(x))
    }).reset_index()

    return countermeasures_grouped

# ---------main------------

product_info = read_product_info('product_info.json')

add_empty_string_to_tags(product_info)

df_controls_from_threats = pd.json_normalize(
    product_info['components'],
    record_path=['usecases', 'threats', 'controls'],
    meta=['name', 'ref', 'tags',
          ['usecases', 'threats', 'ref'],
          ['usecases', 'threats', 'name'],
          ['usecases', 'threats', 'state'],
          ['usecases', 'threats', 'desc'],
          ['usecases', 'threats', 'risk']],
    record_prefix='_', meta_prefix="meta_", max_level=0)

df_controls = pd.json_normalize(
    product_info['components'],
    record_path=['controls'],
    meta=['name', 'ref'],
    record_prefix='_', meta_prefix="meta_", max_level=0)

merged_df = df_controls_from_threats.merge(
    df_controls, left_on=['meta_ref', '_ref'], right_on=['meta_ref', '_ref'], suffixes=('', '_tmp'))

for column in merged_df.columns:
    if column.endswith('_tmp'):
        original_column = column[:-4]
        merged_df[original_column] = merged_df[column]
        merged_df.drop(column, axis=1, inplace=True)

required_tags = read_required_tags_from_config('tmp_config.json')

if required_tags:
    merged_df = merged_df[merged_df['meta_tags'].apply(filter_required_tags, required_tags=required_tags)]
    print (f"\nDF was filtered by the following tags {required_tags}\n")
else:
    print (f"\nNo filtering by tag was applied because required_tags is empty\n")

merged_df = merged_df.sort_values('meta_usecases.threats.risk', ascending=False)

merged_df['meta_usecases.threats.risk'] = pd.cut(merged_df['meta_usecases.threats.risk'], bins=[0, 20, 40, 60, 80, 100], labels=['Very Low', 'Low', 'Medium', 'High', 'Critical'])

merged_df.info()

filtered_data = merged_df[merged_df['meta_usecases.threats.state'] != 'Not Applicable']

# count_and_plot_unique_prefixes(filtered_data, 'threats_type_count.png')
count_and_plot_unique_components(filtered_data, 'threats_by_component_count.png')
count_and_plot_risks(filtered_data, 'risks_chart.png')

table_data = generate_table_data(filtered_data)

countermeasures_grouped = process_countermeasures(merged_df[merged_df['_state'] != 'N/A'])

render_template_to_file(
    template_file='report_template.html',
    output_file='report.html',
    context={
        'table_data': table_data,
        # 'image_path0': 'threats_type_count.png',
        'image_path1': 'threats_by_component_count.png',
        'image_path2': 'risks_chart.png',
        'countermeasures': countermeasures_grouped
}
)
