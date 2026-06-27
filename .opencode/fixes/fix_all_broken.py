#!/usr/bin/env python3
"""
Batch fix ALL remaining broken wiki-links.
Strategy: for each broken target, auto-detect directory and create a stub file.
"""
import os
import re
from collections import Counter
from path_utils import BASE, SKIP_DIRS, walk_markdown

# Build existing file index
existing_base = set()
for root, dirs, files in os.walk(BASE):
    if '.git' in root or '.obsidian' in root or '.ruff_cache' in root:
        continue
    for f in files:
        if f.endswith('.md'):
            existing_base.add(f[:-3])
            rel = os.path.relpath(os.path.join(root, f), BASE).replace('\\', '/')[:-3]
            existing_base.add(rel)

# Scan for broken links
broken_links = Counter()

for root, dirs, files in os.walk(BASE):
    if '.git' in root or '.obsidian' in root or '.ruff_cache' in root:
        continue
    for f in files:
        if not f.endswith('.md'):
            continue
        fpath = os.path.join(root, f)
        rel_source = os.path.relpath(fpath, BASE).replace('\\', '/')
        try:
            with open(fpath, 'r', encoding='utf-8') as fh:
                content = fh.read()
        except:
            continue
        for m in re.finditer(r'\[\[([^\]]+?)\]\]', content):
            target = m.group(1).split('|')[0].split('#')[0].strip()
            if not target or target in ('INDEX', 'LearningPath', 'README', '404'):
                continue
            if target in existing_base or target + '.md' in existing_base:
                continue
            sd = os.path.dirname(rel_source)
            ft = sd + '/' + target
            if ft in existing_base or ft + '.md' in existing_base:
                continue
            broken_links[target] += 1

# Existing directory prefixes for auto-placement
TOPIC_DIR_MAP = {
    # CS topics
    'MachineLearning': '05_ComputerScience/ArtificialIntelligence/MachineLearning',
    'DatabaseSystems': '05_ComputerScience/DatabasesAndInformationSystems',
    'EmbeddedSystems': '05_ComputerScience/HardwareAndEmbeddedSystems',
    'SoftwareEngineering': '05_ComputerScience/SoftwareEngineering',
    'ProgrammingLanguages': '05_ComputerScience/ProgrammingLanguages',
    'BigData': '05_ComputerScience/CloudComputingAndDistributedSystems',
    'DataScience': '07_InterdisciplinarySciences/DataScience',
    'DataMining': '07_InterdisciplinarySciences/DataScience',
    'DataStructures': '05_ComputerScience/DataStructuresAndAlgorithms/DataStructures',
    'Algorithms': '05_ComputerScience/DataStructuresAndAlgorithms/Algorithms',
    'ComputerNetworks': '05_ComputerScience/ComputerNetworks',
    'OperatingSystems': '05_ComputerScience/OperatingSystems',
    'ArtificialIntelligence': '05_ComputerScience/ArtificialIntelligence',
    'NaturalLanguageProcessing': '05_ComputerScience/ArtificialIntelligence/NLP',
    'ComputerVision': '05_ComputerScience/ArtificialIntelligence/ComputerVision',
    'Cybersecurity': '05_ComputerScience/Cybersecurity',
    'CloudComputing': '05_ComputerScience/CloudComputingAndDistributedSystems',
    'Blockchain': '05_ComputerScience/Blockchain',
    'CompilerPrinciples': '05_ComputerScience/CompilerPrinciples',
    'ComputerArchitecture': '05_ComputerScience/ComputerOrganizationAndArchitecture',
    'SoftwareTesting': '05_ComputerScience/SoftwareEngineering/SoftwareTesting',
    'WebDevelopment': '05_ComputerScience/EngineeringDevelopment/WebDevelopment',
    'MobileDevelopment': '05_ComputerScience/EngineeringDevelopment/MobileDevelopment',
    'GameDevelopment': '05_ComputerScience/EngineeringDevelopment/GameDevelopment',
    'DesktopDevelopment': '05_ComputerScience/EngineeringDevelopment/DesktopDevelopment',
    'DevOps': '05_ComputerScience/SoftwareEngineering/DevOpsAndCI_CD',
    'DesignPatterns': '05_ComputerScience/SoftwareEngineering/DesignPatterns',
    'Git': '05_ComputerScience/SoftwareEngineering/GitAndVersionControl',
    'UML': '05_ComputerScience/SoftwareEngineering',
    'Networking': '05_ComputerScience/ComputerNetworks',
    'Cryptography': '05_ComputerScience/Cybersecurity',
    'WebSecurity': '05_ComputerScience/Cybersecurity',
    'Robotics': '05_ComputerScience/HardwareAndEmbeddedSystems/Robotics',
    'IoT': '05_ComputerScience/HardwareAndEmbeddedSystems/IoT',
    'Microcontrollers': '05_ComputerScience/HardwareAndEmbeddedSystems/Microcontrollers',
    'FPGA': '05_ComputerScience/HardwareAndEmbeddedSystems/FPGA',
    'RTOS': '05_ComputerScience/HardwareAndEmbeddedSystems/RTOS',
    'RaspberryPi': '05_ComputerScience/HardwareAndEmbeddedSystems/RaspberryPi',
    'PCB': '05_ComputerScience/HardwareAndEmbeddedSystems/PCB_Design',
    'DigitalCircuits': '05_ComputerScience/HardwareAndEmbeddedSystems/DigitalCircuits',
    'AnalogCircuits': '05_ComputerScience/HardwareAndEmbeddedSystems/AnalogCircuits',
    'SignalProcessing': '04_EngineeringAndTechnology/ElectronicsAndCommunications',
    'ControlSystems': '04_EngineeringAndTechnology/ControlAndSystemsEngineering',
    'Microeconomics': '03_HumanitiesAndSocialSciences/Economics',
    'Macroeconomics': '03_HumanitiesAndSocialSciences/Economics',
    'Econometrics': '03_HumanitiesAndSocialSciences/Economics/Econometrics',
    'BehavioralEconomics': '03_HumanitiesAndSocialSciences/Psychology/BehavioralEconomics',
    'Marketing': '03_HumanitiesAndSocialSciences/Sociology',
    'PublicPolicy': '03_HumanitiesAndSocialSciences/PoliticalScience',
    'InternationalRelations': '03_HumanitiesAndSocialSciences/PoliticalScience',
    'PoliticalPhilosophy': '03_HumanitiesAndSocialSciences/Philosophy',
    'SocialPsychology': '03_HumanitiesAndSocialSciences/Psychology/SocialPsychology',
    'DevelopmentalPsychology': '03_HumanitiesAndSocialSciences/Psychology',
    'ClinicalPsychology': '03_HumanitiesAndSocialSciences/Psychology',
    'CognitiveScience': '07_InterdisciplinarySciences/CognitiveScience',
    'QuantitativeMethods': '07_InterdisciplinarySciences/AppliedStatistics',
    'Probability': '02_NaturalSciences/Mathematics/ProbabilityStatistics',
    'Statistics': '02_NaturalSciences/Mathematics/ProbabilityStatistics',
    'Calculus': '02_NaturalSciences/Mathematics/MathematicalAnalysis',
    'LinearAlgebra': '02_NaturalSciences/Mathematics/Algebra',
    'DifferentialEquations': '02_NaturalSciences/Mathematics/DifferentialEquations',
    'Geometry': '02_NaturalSciences/Mathematics/Geometry',
    'NumberTheory': '02_NaturalSciences/Mathematics/NumberTheory',
    'Topology': '02_NaturalSciences/Mathematics/Topology',
    'DiscreteMath': '02_NaturalSciences/Mathematics',
    'SetTheory': '02_NaturalSciences/Logic',
    'GraphTheory': '02_NaturalSciences/Mathematics',
    'FluidDynamics': '02_NaturalSciences/Physics/ClassicalMechanics',
    'Thermodynamics': '02_NaturalSciences/Physics/Thermodynamics',
    'QuantumMechanics': '02_NaturalSciences/Physics/QuantumMechanics',
    'Electromagnetism': '02_NaturalSciences/Physics/Electromagnetism',
    'Optics': '02_NaturalSciences/Physics/Optics',
    'ParticlePhysics': '02_NaturalSciences/Physics/ParticlePhysics',
    'Relativity': '02_NaturalSciences/Physics/Relativity',
    'Astrophysics': '02_NaturalSciences/Astronomy',
    'Geology': '02_NaturalSciences/EarthSciences',
    'Oceanography': '02_NaturalSciences/EarthSciences',
    'Meteorology': '02_NaturalSciences/EarthSciences',
    'Climatology': '02_NaturalSciences/EarthSciences',
    'Ecology': '02_NaturalSciences/Biology',
    'Evolution': '02_NaturalSciences/Biology',
    'Genetics': '02_NaturalSciences/Biology/Genetics',
    'CellBiology': '02_NaturalSciences/Biology/CellBiology',
    'MolecularBiology': '02_NaturalSciences/Biology/MolecularBiology',
    'Biochemistry': '02_NaturalSciences/Chemistry/Biochemistry',
    'OrganicChemistry': '02_NaturalSciences/Chemistry/OrganicChemistry',
    'InorganicChemistry': '02_NaturalSciences/Chemistry/InorganicChemistry',
    'PhysicalChemistry': '02_NaturalSciences/Chemistry/PhysicalChemistry',
    'AnalyticalChemistry': '02_NaturalSciences/Chemistry/AnalyticalChemistry',
    'MedicinalChemistry': '09_MedicineAndHealth/Pharmacy',
    'Pharmacology': '09_MedicineAndHealth/BasicMedicalSciences',
    'Physiology': '09_MedicineAndHealth/BasicMedicalSciences',
    'Anatomy': '09_MedicineAndHealth/BasicMedicalSciences',
    'Pathology': '09_MedicineAndHealth/BasicMedicalSciences',
    'Immunology': '09_MedicineAndHealth/BasicMedicalSciences',
    'Microbiology': '09_MedicineAndHealth/BasicMedicalSciences',
    'Neuroscience': '09_MedicineAndHealth/BasicMedicalSciences',
    'Psychology': '03_HumanitiesAndSocialSciences/Psychology',
    'Sociology': '03_HumanitiesAndSocialSciences/Sociology',
    'Anthropology': '03_HumanitiesAndSocialSciences/Anthropology',
    'Archaeology': '03_HumanitiesAndSocialSciences/Archaeology',
    'Linguistics': '03_HumanitiesAndSocialSciences/Linguistics',
    'Philosophy': '03_HumanitiesAndSocialSciences/Philosophy',
    'History': '03_HumanitiesAndSocialSciences/History',
    'WorldHistory': '03_HumanitiesAndSocialSciences/History',
    'ArtHistory': '06_ArtsAndCreativity/FineArts/ArtHistory',
    'MusicTheory': '06_ArtsAndCreativity/Music/MusicTheory',
    'MusicHistory': '06_ArtsAndCreativity/Music/MusicHistory',
    'Harmony': '06_ArtsAndCreativity/Music/Harmony',
    'Nutrition': '09_MedicineAndHealth/PublicHealth',
    'ExercisePhysiology': '12_SportsScience/ExercisePhysiology',
    'SportsMedicine': '12_SportsScience/SportsMedicine',
    'PhysicalTherapy': '12_SportsScience/SportsMedicine',
    'StrengthTraining': '12_SportsScience/SportsTraining',
    'EnduranceTraining': '12_SportsScience/SportsTraining',
    'ProjectManagement': '11_ManagementSciences/ManagementScienceAndEngineering',
    'SupplyChain': '11_ManagementSciences/ManagementScienceAndEngineering',
    'QualityManagement': '11_ManagementSciences/ManagementScienceAndEngineering',
    'OperationsResearch': '11_ManagementSciences/ManagementScienceAndEngineering',
    'InnovationManagement': '11_ManagementSciences/ManagementScienceAndEngineering',
    'HumanResources': '11_ManagementSciences/BusinessAdministration/HumanResources',
    'Accounting': '11_ManagementSciences/BusinessAdministration/Accounting',
    'Finance': '11_ManagementSciences/BusinessAdministration/Finance',
    'FinancialMarkets': '11_ManagementSciences/BusinessAdministration/Finance',
    'CorporateFinance': '11_ManagementSciences/BusinessAdministration/Finance',
    'Investment': '11_ManagementSciences/BusinessAdministration/Finance',
    'RiskManagement': '11_ManagementSciences/BusinessAdministration/Finance',
    'MarketingStrategy': '11_ManagementSciences/BusinessAdministration/Marketing',
    'BrandManagement': '11_ManagementSciences/BusinessAdministration/Marketing',
    'ConsumerBehavior': '11_ManagementSciences/BusinessAdministration/Marketing',
    'DigitalMarketing': '11_ManagementSciences/BusinessAdministration/Marketing',
    'PublicAdministration': '11_ManagementSciences/PublicAdministration',
    'LibraryScience': '11_ManagementSciences/LibraryAndArchive',
    'InformationScience': '11_ManagementSciences/LibraryAndArchive',
    'KnowledgeManagement': '11_ManagementSciences/LibraryAndArchive',
    'TimeManagement': '13_Others/PersonalProductivity/TimeManagement',
    'CriticalThinking': '00_KnowledgeFramework/Methodology',
    'AcademicWriting': '13_Others/AcademicWriting',
    'ResearchMethods': '00_KnowledgeFramework/Methodology',
    'NoteTaking': '00_KnowledgeFramework/NoteTaking',
    'KnowledgeGraph': '00_KnowledgeFramework/KnowledgeGraph',
    'LearningPaths': '00_KnowledgeFramework/LearningPaths',
    'ChemicalEngineering': '04_EngineeringAndTechnology/ChemicalAndPharmaceuticalEngineering',
    'MechanicalEngineering': '04_EngineeringAndTechnology/MechanicalAndElectricalEngineering/MechanicalEngineering',
    'ElectricalEngineering': '04_EngineeringAndTechnology/MechanicalAndElectricalEngineering/ElectricalEngineering',
    'CivilEngineering': '04_EngineeringAndTechnology/CivilEngineering',
    'MaterialsScience': '04_EngineeringAndTechnology/MechanicsAndMaterials/MaterialsScience',
    'EnvironmentalEngineering': '04_EngineeringAndTechnology/EnvironmentalScienceAndEngineering',
    'AerospaceEngineering': '04_EngineeringAndTechnology/AerospaceAndMilitaryEngineering/AerospaceEngineering',
    'StructuralEngineering': '04_EngineeringAndTechnology/CivilEngineering',
    'DataVisualization': '07_InterdisciplinarySciences/DataScience',
    'TimeSeries': '07_InterdisciplinarySciences/AppliedStatistics',
    'BayesianStatistics': '07_InterdisciplinarySciences/AppliedStatistics',
    'RegressionAnalysis': '07_InterdisciplinarySciences/AppliedStatistics',
    'MachineLearningAlgorithms': '05_ComputerScience/ArtificialIntelligence/MachineLearning',
    'DeepLearning': '05_ComputerScience/ArtificialIntelligence/MachineLearning/NeuralNetworksAndDeepLearning',
    'NeuralNetworks': '05_ComputerScience/ArtificialIntelligence/MachineLearning/NeuralNetworksAndDeepLearning',
    'ReinforcementLearning': '05_ComputerScience/ArtificialIntelligence/MachineLearning/ReinforcementLearning',
    'SupervisedLearning': '05_ComputerScience/ArtificialIntelligence/MachineLearning/SupervisedLearning',
    'UnsupervisedLearning': '05_ComputerScience/ArtificialIntelligence/MachineLearning/UnsupervisedLearning',
    'NLP': '05_ComputerScience/ArtificialIntelligence/NLP',
    'ComputerGraphics': '05_ComputerScience/ComputerGraphicsAndVision',
    'HumanComputerInteraction': '05_ComputerScience/HumanComputerInteraction',
    'DistributedSystems': '05_ComputerScience/CloudComputingAndDistributedSystems',
    'ParallelComputing': '05_ComputerScience/CloudComputingAndDistributedSystems',
    'DatabaseManagement': '05_ComputerScience/DatabasesAndInformationSystems',
    'InformationRetrieval': '05_ComputerScience/DatabasesAndInformationSystems/InformationRetrieval',
    'DataWarehousing': '05_ComputerScience/DatabasesAndInformationSystems/DataWarehousing',
    'BigDataAnalytics': '07_InterdisciplinarySciences/DataScience/BigDataAnalytics',
    'AIGC': '05_ComputerScience/ArtificialIntelligence/AIGC',
    'KnowledgeRepresentation': '05_ComputerScience/ArtificialIntelligence/KnowledgeRepresentation',
    'ComputerVision': '05_ComputerScience/ArtificialIntelligence/ComputerVision',
    'ComputationalLinguistics': '07_InterdisciplinarySciences/DigitalHumanities',
    'DigitalHumanities': '07_InterdisciplinarySciences/DigitalHumanities',
    'Bioinformatics': '07_InterdisciplinarySciences/Bioinformatics',
    'ComputationalBiology': '07_InterdisciplinarySciences/Bioinformatics',
    'Genomics': '02_NaturalSciences/Biology/Genetics',
    'Biophysics': '02_NaturalSciences/Biology',
    'SystemsBiology': '07_InterdisciplinarySciences/Bioinformatics',
    'QuantumComputing': '07_InterdisciplinarySciences/QuantumInformationScience',
    'QuantumInformation': '07_InterdisciplinarySciences/QuantumInformationScience',
    'QuantumCryptography': '07_InterdisciplinarySciences/QuantumInformationScience',
    'Nanotechnology': '04_EngineeringAndTechnology/Biotechnologies',
    'Biomaterials': '04_EngineeringAndTechnology/Biotechnologies',
    'AgriculturalEconomics': '08_AgriculturalSciences/AgriculturalResources',
    'CropScience': '08_AgriculturalSciences/CropScience',
    'AnimalScience': '08_AgriculturalSciences/AnimalScience',
    'FoodScience': '08_AgriculturalSciences/FoodScience',
    'EnvironmentalScience': '07_InterdisciplinarySciences/EnvironmentalScience',
    'PublicHealth': '09_MedicineAndHealth/PublicHealth',
    'Epidemiology': '09_MedicineAndHealth/PublicHealth',
    'Biostatistics': '09_MedicineAndHealth/PublicHealth',
    'TraditionalChineseMedicine': '09_MedicineAndHealth/TraditionalChineseMedicine',
    'Pharmaceutics': '09_MedicineAndHealth/Pharmacy',
    'ClinicalPharmacy': '09_MedicineAndHealth/Pharmacy',
    'Pharmacognosy': '09_MedicineAndHealth/Pharmacy',
    'MilitaryStrategy': '10_MilitarySciences/MilitaryStrategy',
    'MilitaryHistory': '10_MilitarySciences/MilitaryHistory',
    'SportsNutrition': '12_SportsScience/SportsMedicine',
    'ExerciseBiochemistry': '12_SportsScience/ExercisePhysiology',
    'SportsPsychology': '12_SportsScience/SportsTraining',
    'Periodization': '12_SportsScience/SportsTraining',
    'SportsInjuries': '12_SportsScience/SportsMedicine',
    'Rehabilitation': '12_SportsScience/SportsMedicine',
    'RehabilitationTherapy': '12_SportsScience/SportsMedicine',
    'SportsMassage': '12_SportsScience/SportsMedicine',
    'Doping': '12_SportsScience/SportsMedicine',
    'PhysicalEducation': '12_SportsScience/PhysicalEducation',
    'MotorLearning': '12_SportsScience/PhysicalEducation',
    'CurriculumDesign': '12_SportsScience/PhysicalEducation',
    'TeachingMethods': '12_SportsScience/PhysicalEducation',
    'AdaptedPE': '12_SportsScience/PhysicalEducation',
}

# Create stubs for broken links
created = 0
skipped = 0
for target, count in broken_links.most_common():
    # Skip INDEX references (they work in Obsidian)
    if '/INDEX' in target or target.endswith('/INDEX'):
        skipped += 1
        continue
    
    # Determine directory
    if target in TOPIC_DIR_MAP:
        dir_path = os.path.join(BASE, TOPIC_DIR_MAP[target])
    else:
        # Try to match by prefix
        matched = False
        for prefix, base_dir in sorted(TOPIC_DIR_MAP.items(), key=lambda x: -len(x[0])):
            if target.startswith(prefix):
                dir_path = os.path.join(BASE, base_dir)
                matched = True
                break
        if not matched:
            dir_path = os.path.join(BASE, '_Stubs')
    
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, target + '.md')
    
    if os.path.exists(file_path):
        skipped += 1
        continue
    
    # Build tag list from path
    rel_dir = os.path.relpath(dir_path, BASE).replace('\\', '/')
    tags_parts = rel_dir.split('/')
    tag_str = ', '.join(["'" + p + "'" for p in tags_parts if p and p != '_Stubs'])
    if not tag_str:
        tag_str = "'_Stubs'"
    
    # Skip garbled targets (non-printable or pure gibberish)
    non_ascii = sum(1 for c in target if ord(c) > 127)
    if non_ascii > len(target) * 0.5 and not all(c.isalpha() or c in '-_' for c in target if ord(c) > 127):
        skipped += 1
        continue
    
    # Handle edge case: don't create files with path separators in target name
    if '/' in target or '\\' in target:
        skipped += 1
        continue
    
    # Create the file
    content = '---\n'
    content += f'aliases: [{target}]\n'
    content += f'tags: [{tag_str}]\n'
    content += '---\n\n'
    content += f'# {target}\n\n'
    content += '> 此页面内容待完善。\n\n'
    content += '## 相关条目\n'
    # Add backlink suggestions based on the topic
    related = []
    for prefix, base_dir in sorted(TOPIC_DIR_MAP.items(), key=lambda x: -len(x[0])):
        if target.startswith(prefix) and prefix != target:
            related.append(f'- [[{prefix}]]\n')
            break
    if not related:
        # Try to add parent topic
        parent = '/'.join(rel_dir.split('/')[-2:]) if '/' in rel_dir else rel_dir
        if parent and parent != '_Stubs':
            content += f'- [[{parent}/INDEX|{parent} 索引]]\n'
    content += f'- [[INDEX|当前目录索引]]\n'
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    created += 1
    if created <= 10 or count >= 3:
        print(f'[CREATE] {rel_dir}/{target}.md (refs: {count})')

print(f'\nDone! Created: {created}, Skipped (exists/INDEX): {skipped}')
