import json
import os
import shutil
import rdflib
import logging
import argparse
from rdflib.namespace import RDF, XSD, DCTERMS, RDFS, DCAT

PMD = rdflib.Namespace('https://w3id.org/pmd/co/')
TTO = rdflib.Namespace('https://w3id.org/pmd/tto/')
QUDT = rdflib.Namespace('https://qudt.org/vocab/unit/')

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--namespace', required=True, help='Namespace for the ABox')
parser.add_argument('-r', '--resources_namespace', required=False, default=None, help='Namespace for resources, defaults to <--namespace>/resources/')
args = parser.parse_args()

EX = rdflib.Namespace(args.namespace)

if args.resources_namespace is None:
    resources_namespace_ = args.namespace+'resources/'
else:
    resources_namespace_ = args.resources_namespace

g = rdflib.Graph()

g.bind('pmd', PMD)
g.bind('tto', TTO)
g.bind('qudt', QUDT)
g.bind('', EX)

def _add_resource(filename):
    if os.path.exists(f'original_data/{filename}'):
        if not os.path.exists('resources'):
            os.mkdir('resources')
        shutil.copyfile(f'original_data/{filename}', f'resources/{filename}')
    else:
        logging.warning('File %s was not found in the original_data directory. In gh-pages it will show up as empty file.', filename)

with open('refdataproject_production.json', 'r', encoding='utf8') as f:
    data = json.load(f)

rod = rdflib.URIRef(f'{args.namespace}rod')
g.add((rod, RDF.type, PMD.BaseMaterial))
g.add((rod, RDFS.label, rdflib.Literal('Rod material', lang='en')))
g.add((rod, PMD.characteristic, rod_inspection_certificate := rdflib.BNode()))
g.add((rod, PMD.characteristic, rod_material_designation := rdflib.BNode()))
g.add((rod_material_designation, RDF.type, PMD.MaterialDesignation))
g.add((rod_material_designation, RDF.type, PMD.Metadata))
g.add((rod_material_designation, PMD.value, rdflib.Literal('42CrMoS4', datatype=XSD.string)))
g.add((rod_material_designation, PMD.relatesTo, rod_material_standard := rdflib.BNode()))
g.add((rod_material_standard, RDF.type, PMD.Norm))
g.add((rod_material_standard, RDF.type, PMD.Metadata))
g.add((rod_material_standard, PMD.value, rdflib.Literal('DIN EN 10083:2006', datatype=XSD.string)))
g.add((rod_inspection_certificate, RDF.type, PMD.InspectionDocument))
g.add((rod_inspection_certificate, RDF.type, PMD.Metadata))
g.add((rod_inspection_certificate, PMD.resource, rod_inspection_certificate_resource := rdflib.BNode()))
g.add((rod_inspection_certificate_resource, RDF.type, PMD.Dataset))
g.add((rod_inspection_certificate_resource, RDF.type, DCAT.Dataset))
g.add((rod_inspection_certificate_resource, DCAT.distribution, rod_inspection_certificate_resource_dist := rdflib.BNode()))
g.add((rod_inspection_certificate_resource_dist, RDF.type, DCAT.Distribution))
g.add((rod_inspection_certificate_resource_dist, DCAT.downloadURL, rdflib.Literal(f"{resources_namespace_}rod_inspection_certificate_anon.pdf", datatype=XSD.anyURI)))
g.add((rod_inspection_certificate_resource_dist, DCAT.mediaType, rdflib.Literal("application/pdf", datatype=XSD.string)))
g.add((rod_inspection_certificate_resource_dist, DCTERMS.format, rod_inspection_certificate_resource_dist_fmt := rdflib.BNode()))
g.add((rod_inspection_certificate_resource_dist_fmt, RDFS.label, rdflib.Literal("PDF", datatype=XSD.string)))
_add_resource('rod_inspection_certificate_anon.pdf')

def spec_ht(temp, charge):
    heattreatment_recipe = rdflib.URIRef(EX.term(f"recipe_heattreatment_{int(temp)}"))
    heattreatment_austemp = rdflib.BNode()
    heattreatment_austemp_note = rdflib.BNode()
    g.add((heattreatment_recipe, RDF.type, PMD.Document))
    g.add((heattreatment_recipe, RDF.type, PMD.Metadata))
    g.add((heattreatment_recipe, PMD.characteristic, ht_Q_protocol_pdf := rdflib.BNode()))
    g.add((heattreatment_recipe, PMD.characteristic, ht_Q_protocol_csv := rdflib.BNode()))
    g.add((heattreatment_recipe, PMD.characteristic, ht_T_protocol_pdf := rdflib.BNode()))
    g.add((heattreatment_recipe, PMD.characteristic, ht_T_protocol_csv := rdflib.BNode()))
    g.add((ht_Q_protocol_pdf, RDF.type, PMD.Document))
    g.add((ht_Q_protocol_pdf, RDF.type, PMD.Metadata))
    g.add((ht_Q_protocol_pdf, PMD.resource, ht_Q_protocol_pdf_resource := rdflib.BNode()))
    g.add((ht_Q_protocol_pdf_resource, RDF.type, PMD.Dataset))
    g.add((ht_Q_protocol_pdf_resource, RDF.type, DCAT.Dataset))
    g.add((ht_Q_protocol_pdf_resource, DCAT.distribution, ht_Q_protocol_pdf_resource_dist := rdflib.BNode()))
    g.add((ht_Q_protocol_pdf_resource_dist, RDF.type, DCAT.Distribution))
    g.add((ht_Q_protocol_pdf_resource_dist, DCAT.downloadURL, rdflib.Literal(f"{resources_namespace_}HT_Q_Charge_{charge:d}.pdf", datatype=XSD.anyURI)))
    g.add((ht_Q_protocol_pdf_resource_dist, DCAT.mediaType, rdflib.Literal("application/pdf", datatype=XSD.string)))
    g.add((ht_Q_protocol_pdf_resource_dist, DCTERMS.format, ht_Q_protocol_pdf_resource_dist_fmt := rdflib.BNode()))
    g.add((ht_Q_protocol_pdf_resource_dist_fmt, RDFS.label, rdflib.Literal("PDF", datatype=XSD.string)))
    g.add((ht_Q_protocol_csv, RDF.type, PMD.Document))
    g.add((ht_Q_protocol_csv, RDF.type, PMD.Metadata))
    g.add((ht_Q_protocol_csv, PMD.resource, ht_Q_protocol_csv_resource := rdflib.BNode()))
    g.add((ht_Q_protocol_csv_resource, RDF.type, PMD.Dataset))
    g.add((ht_Q_protocol_csv_resource, RDF.type, DCAT.Dataset))
    g.add((ht_Q_protocol_csv_resource, DCAT.distribution, ht_Q_protocol_csv_resource_dist := rdflib.BNode()))
    g.add((ht_Q_protocol_csv_resource_dist, RDF.type, DCAT.Distribution))
    g.add((ht_Q_protocol_csv_resource_dist, DCAT.downloadURL, rdflib.Literal(f"{resources_namespace_}resources/HT_Q_Charge_{charge:d}.csv", datatype=XSD.anyURI)))
    g.add((ht_Q_protocol_csv_resource_dist, DCAT.mediaType, rdflib.Literal("text/csv", datatype=XSD.string)))
    g.add((ht_Q_protocol_csv_resource_dist, DCTERMS.format, ht_Q_protocol_csv_resource_dist_fmt := rdflib.BNode()))
    g.add((ht_Q_protocol_csv_resource_dist_fmt, RDFS.label, rdflib.Literal("CSV", datatype=XSD.string)))
    g.add((ht_T_protocol_pdf, RDF.type, PMD.Document))
    g.add((ht_T_protocol_pdf, RDF.type, PMD.Metadata))
    g.add((ht_T_protocol_pdf, PMD.resource, ht_T_protocol_pdf_resource := rdflib.BNode()))
    g.add((ht_T_protocol_pdf_resource, RDF.type, PMD.Dataset))
    g.add((ht_T_protocol_pdf_resource, RDF.type, DCAT.Dataset))
    g.add((ht_T_protocol_pdf_resource, DCAT.distribution, ht_T_protocol_pdf_resource_dist := rdflib.BNode()))
    g.add((ht_T_protocol_pdf_resource_dist, RDF.type, DCAT.Distribution))
    g.add((ht_T_protocol_pdf_resource_dist, DCAT.downloadURL, rdflib.Literal(f"{resources_namespace_}HT_T.pdf", datatype=XSD.anyURI)))
    g.add((ht_T_protocol_pdf_resource_dist, DCAT.mediaType, rdflib.Literal("application/pdf", datatype=XSD.string)))
    g.add((ht_T_protocol_pdf_resource_dist, DCTERMS.format, ht_T_protocol_pdf_resource_dist_fmt := rdflib.BNode()))
    g.add((ht_T_protocol_pdf_resource_dist_fmt, RDFS.label, rdflib.Literal("PDF", datatype=XSD.string)))
    g.add((ht_T_protocol_csv, RDF.type, PMD.Document))
    g.add((ht_T_protocol_csv, RDF.type, PMD.Metadata))
    g.add((ht_T_protocol_csv, PMD.resource, ht_T_protocol_csv_resource := rdflib.BNode()))
    g.add((ht_T_protocol_csv_resource, RDF.type, PMD.Dataset))
    g.add((ht_T_protocol_csv_resource, RDF.type, DCAT.Dataset))
    g.add((ht_T_protocol_csv_resource, DCAT.distribution, ht_T_protocol_csv_resource_dist := rdflib.BNode()))
    g.add((ht_T_protocol_csv_resource_dist, RDF.type, DCAT.Distribution))
    g.add((ht_T_protocol_csv_resource_dist, DCAT.downloadURL, rdflib.Literal(f"{resources_namespace_}HT_T.csv", datatype=XSD.anyURI)))
    g.add((ht_T_protocol_csv_resource_dist, DCAT.mediaType, rdflib.Literal("text/csv", datatype=XSD.string)))
    g.add((ht_T_protocol_csv_resource_dist, DCTERMS.format, ht_T_protocol_csv_resource_dist_fmt := rdflib.BNode()))
    g.add((ht_T_protocol_csv_resource_dist_fmt, RDFS.label, rdflib.Literal("CSV", datatype=XSD.string)))
    g.add((heattreatment_recipe, PMD.characteristic, heattreatment_austemp))
    g.add((heattreatment_austemp, RDF.type, PMD.Temperature))
    g.add((heattreatment_austemp, RDF.type, PMD.Metadata))
    g.add((heattreatment_austemp, PMD.value, rdflib.Literal(float(temp), datatype=XSD.float)))
    g.add((heattreatment_austemp, PMD.unit, QUDT.CELSIUS))
    g.add((heattreatment_austemp, PMD.characteristic, heattreatment_austemp_note))
    g.add((heattreatment_austemp_note, RDF.type, PMD.Note))
    g.add((heattreatment_austemp_note, PMD.value, rdflib.Literal("Austenitisation temperature", lang="en")))
    _add_resource(f'HT_Q_Charge_{charge:d}.pdf')
    _add_resource(f'HT_Q_Charge_{charge:d}.csv')
    return heattreatment_recipe
heattreatment_recipes = {t: spec_ht(t, c) for t, c in [(850, 3466), (925, 3467), (1000, 3468), (1075, 3471), (1150, 3470)]}
_add_resource('HT_T.pdf')
_add_resource('HT_T.csv')

shipping = EX.term("process_shipping")
shipping_sticker = rdflib.BNode()
shipping_sticker_resource = rdflib.BNode()
shipping_sticker_resource_dist = rdflib.BNode()
shipping_sticker_resource_dist_fmt = rdflib.BNode()
g.add((shipping, RDF.type, PMD.Process))
g.add((shipping, PMD.characteristic, shipping_sticker))
g.add((shipping_sticker, RDF.type, PMD.Document))
g.add((shipping_sticker, RDF.type, PMD.Metadata))
g.add((shipping_sticker, PMD.resource, shipping_sticker_resource))
g.add((shipping_sticker_resource, RDF.type, PMD.Dataset))
g.add((shipping_sticker_resource, RDF.type, DCAT.Dataset))
g.add((shipping_sticker_resource, DCAT.distribution, shipping_sticker_resource_dist))
g.add((shipping_sticker_resource_dist, RDF.type, DCAT.Distribution))
g.add((shipping_sticker_resource_dist, DCAT.downloadURL, rdflib.Literal(f"{resources_namespace_}shipping_sticker_anon.pdf", datatype=XSD.anyURI)))
g.add((shipping_sticker_resource_dist, DCAT.mediaType, rdflib.Literal("application/pdf", datatype=XSD.string)))
g.add((shipping_sticker_resource_dist, DCTERMS.format, shipping_sticker_resource_dist_fmt))
g.add((shipping_sticker_resource_dist_fmt, RDFS.label, rdflib.Literal("PDF", datatype=XSD.string)))
_add_resource('shipping_sticker_anon.pdf')

for path in data:
    blank_iwt = EX.term(f"blank_iwt_{path['blank_id_iwt']}")
    blank_id_iwt = rdflib.BNode()
    g.add((blank_iwt, RDF.type, PMD.Blank))
    g.add((blank_iwt, PMD.characteristic, blank_id_iwt))
    g.add((blank_id_iwt, RDF.type, PMD.Identifier))
    g.add((blank_id_iwt, RDF.type, PMD.Metadata))
    g.add((blank_id_iwt, PMD.value, rdflib.Literal(path['blank_id_iwt'], datatype=XSD.string)))

    blank_iwm = EX.term(f"blank_iwt_{path['blank_id']}")
    blank_id_iwm = rdflib.BNode()
    g.add((blank_iwm, RDF.type, PMD.Blank))
    g.add((blank_iwm, PMD.characteristic, blank_id_iwm))
    g.add((blank_id_iwm, RDF.type, PMD.Identifier))
    g.add((blank_id_iwm, RDF.type, PMD.Metadata))
    g.add((blank_id_iwm, PMD.value, rdflib.Literal(path['blank_id'], datatype=XSD.string)))

    tensile_specimen = EX.term(f"specimen_{path['tensile_specimen_id']}")
    metallo_disc = EX.term(f"specimen_{path['metallo_disc_id']}")

    cutting1 = EX.term(f"process_cutting1_{path['blank_id_iwt']}")
    cutting1_id = rdflib.BNode()
    g.add((cutting1, RDF.type, PMD.ManufacturingProcess))
    g.add((cutting1, PMD.characteristic, cutting1_id))
    g.add((cutting1_id, RDF.type, PMD.ProcessIdentifier))
    g.add((cutting1_id, PMD.value, rdflib.Literal(f"process_cutting1_{path['blank_id_iwt']}", datatype=XSD.string)))
    g.add((cutting1, PMD.input, rod))
    g.add((cutting1, PMD.output, blank_iwt))

    heattreatment = rdflib.URIRef(EX.term(f"process_heattreatment_{path['blank_id']}"))
    heattreatment_id = rdflib.BNode()
    g.add((heattreatment, RDF.type, PMD.HeatTreatmentProcess))
    g.add((heattreatment, PMD.characteristic, heattreatment_id))
    g.add((heattreatment_id, RDF.type, PMD.ProcessIdentifier))
    g.add((heattreatment_id, PMD.value, rdflib.Literal(f"process_heattreatment_{path['blank_id']}", datatype=XSD.string)))
    g.add((heattreatment, PMD.input, blank_iwm))
    g.add((heattreatment, PMD.output, blank_iwm))
    g.add((heattreatment, PMD.characteristic, heattreatment_recipes[int(path['aust_temp'])]))
    g.add((heattreatment, PMD.previousProcess, cutting1))
    g.add((cutting1, PMD.nextProcess, heattreatment))

    shipping_sub = EX.term(f"process_shipping_{path['blank_id_iwt']}")
    g.add((shipping_sub, RDF.type, PMD.Process))
    g.add((shipping_sub, PMD.superordinateProcess, shipping))
    g.add((shipping_sub, PMD.input, blank_iwt))
    g.add((shipping_sub, PMD.output, blank_iwm))
    g.add((shipping_sub, PMD.previousProcess, heattreatment))
    g.add((heattreatment, PMD.nextProcess, shipping_sub))

    cutting2 = rdflib.URIRef(EX.term(f"process_cutting2_{path['blank_id']}"))
    cutting2_id = rdflib.BNode()
    g.add((cutting2, RDF.type, PMD.ManufacturingProcess))
    g.add((cutting2, PMD.characteristic, cutting2_id))
    g.add((cutting2_id, RDF.type, PMD.ProcessIdentifier))
    g.add((cutting2_id, PMD.value, rdflib.Literal(f"process_cutting2_{path['blank_id']}", datatype=XSD.string)))
    g.add((cutting2, PMD.input, blank_iwm))
    g.add((cutting2, PMD.output, tensile_specimen))
    g.add((cutting2, PMD.output, metallo_disc))
    g.add((cutting2, PMD.previousProcess, shipping_sub))
    g.add((shipping_sub, PMD.nextProcess, cutting2))

    tensile_test = EX.term(f"tensile_test_{path['tensile_specimen_id']}")
    metallo_embedding = EX.term(f"metallo_embedding_{path['metallo_disc_id']}")

    g.add((cutting2, PMD.nextProcess, tensile_test))
    g.add((tensile_test, PMD.previousProcess, cutting2))
    g.add((cutting2, PMD.nextProcess, metallo_embedding))
    g.add((metallo_embedding, PMD.previousProcess, cutting2))

g.serialize('refdataproject_production.ttl', format='turtle')
