// -*- C++ -*-
//
// This file is part of HepMC
// Copyright (C) 2014-2019 The HepMC collaboration (see AUTHORS for details)
//
/// @example convert_example.cc
/// @brief Utility to convert between different types of event records
///
#include "HepMC3/Print.h"
#include "HepMC3/GenEvent.h"
#include "HepMC3/ReaderAsciiHepMC2.h"
#include "HepMC3/WriterAsciiHepMC2.h"
#include "HepMC3/ReaderAscii.h"
#include "HepMC3/WriterAscii.h"
#include "HepMC3/WriterHEPEVT.h"
#include "HepMC3/ReaderHEPEVT.h"
#include "HepMC3/ReaderLHEF.h"

#ifdef HEPMC3_ROOTIO
#include "HepMC3/ReaderRoot.h"
#include "HepMC3/WriterRoot.h"
#include "HepMC3/ReaderRootTree.h"
#include "HepMC3/WriterRootTree.h"
#endif

/* Extension example*/
#ifdef HEPMCCONVERT_EXTENSION_ROOTTREEOPAL
#ifndef HEPMC3_ROOTIO
#warning "HEPMCCONVERT_EXTENSION_ROOTTREEOPAL requires  compilation with of HepMC with ROOT, i.e. HEPMC3_ROOTIO.This extension will be disabled."
#undef HEPMCCONVERT_EXTENSION_ROOTTREEOPAL
#else
#include "WriterRootTreeOPAL.h"
#endif
#endif
#ifdef HEPMCCONVERT_EXTENSION_HEPEVTZEUS
#include "WriterHEPEVTZEUS.h"
#endif
#ifdef HEPMCCONVERT_EXTENSION_DOT
#include "WriterDOT.h"
#endif
#ifdef HEPMCCONVERT_EXTENSION_GZ
#include "ReaderGZ.h"
#endif



#include "cmdline.h"
using namespace HepMC3;
enum formats {hepmc2, hepmc3, hpe ,root, treeroot ,treerootopal, hpezeus, lhef, dump, dot, gz, none};
int main(int argc, char** argv)
{
    gengetopt_args_info ai;
    if (cmdline_parser (argc, argv, &ai) != 0) {
        exit(1);
    }
    if (ai.inputs_num!=2)
    {
        printf("Exactly two arguments are requred: the name of input and output files\n");
        exit(1);
    }
    std::map<std::string,formats> format_map;
    format_map.insert(std::pair<std::string,formats> ( "hepmc2", hepmc2 ));
    format_map.insert(std::pair<std::string,formats> ( "hepmc3", hepmc3 ));
    format_map.insert(std::pair<std::string,formats> ( "hpe", hpe  ));
    format_map.insert(std::pair<std::string,formats> ( "root", root ));
    format_map.insert(std::pair<std::string,formats> ( "treeroot", treeroot ));
    format_map.insert(std::pair<std::string,formats> ( "treerootopal", treerootopal ));
    format_map.insert(std::pair<std::string,formats> ( "hpezeus", hpezeus ));
    format_map.insert(std::pair<std::string,formats> ( "lhef", lhef ));
    format_map.insert(std::pair<std::string,formats> ( "dump", dump ));
    format_map.insert(std::pair<std::string,formats> ( "dot", dot ));
    format_map.insert(std::pair<std::string,formats> ( "gz", gz ));
    format_map.insert(std::pair<std::string,formats> ( "none", none ));
    std::map<std::string, std::string> options;
    for (size_t i=0; i<ai.extensions_given; i++)
    {
        std::string optarg=std::string(ai.extensions_arg[i]);
        size_t pos=optarg.find_first_of('=');
        if (pos<optarg.length())
            options[std::string(optarg,0,pos)]=std::string(optarg,pos+1,optarg.length());
    }
    long int  events_parsed = 0;
    long int  events_limit = ai.events_limit_arg;
    long int  first_event_number = ai.first_event_number_arg;
    long int  last_event_number = ai.last_event_number_arg;
    long int  print_each_events_parsed = ai.print_every_events_parsed_arg;
    Reader*      input_file=0;
    bool ignore_writer=false;
    switch (format_map.at(std::string(ai.input_format_arg)))
    {
    case hepmc2:
        input_file=new ReaderAsciiHepMC2(ai.inputs[0]);
        break;
    case hepmc3:
        input_file=new ReaderAscii(ai.inputs[0]);
        break;
    case hpe:
        input_file=new ReaderHEPEVT(ai.inputs[0]);
        break;
    case lhef:
        input_file=new ReaderLHEF(ai.inputs[0]);
        break;
    case gz:
#ifdef HEPMCCONVERT_EXTENSION_GZ
        input_file=new ReaderGZ(ai.inputs[0]);
        break;
#else
        printf("Input format %s  is not supported\n",ai.input_format_arg);
        exit(2);
#endif
    case treeroot:
#ifdef HEPMC3_ROOTIO
        input_file=new ReaderRootTree(ai.inputs[0]);
        break;
#else
        printf("Input format %s  is not supported\n",ai.input_format_arg);
        exit(2);
#endif
    case root:
#ifdef HEPMC3_ROOTIO
        input_file=new ReaderRoot(ai.inputs[0]);
        break;
#else
        printf("Input format %s  is not supported\n",ai.input_format_arg);
        exit(2);
#endif
    default:
        printf("Input format %s  is not known\n",ai.input_format_arg);
        exit(2);
        break;
    }
    Writer*      output_file=0;
    switch (format_map.at(std::string(ai.output_format_arg)))
    {
    case hepmc2:
        output_file=new WriterAsciiHepMC2(ai.inputs[1]);
        break;
    case hepmc3:
        output_file=new WriterAscii(ai.inputs[1]);
        break;
    case hpe:
        output_file=new WriterHEPEVT(ai.inputs[1]);
        break;
    case root:
#ifdef HEPMC3_ROOTIO
        output_file=new WriterRoot(ai.inputs[1]);
        break;
#else
        printf("Output format %s  is not supported\n",ai.output_format_arg);
        exit(2);
#endif
    case treeroot:
#ifdef HEPMC3_ROOTIO
        output_file=new WriterRootTree(ai.inputs[1]);
        break;
#else
        printf("Output format %s  is not supported\n",ai.output_format_arg);
        exit(2);
#endif
    /* Extension example*/
    case treerootopal:
#ifdef HEPMCCONVERT_EXTENSION_ROOTTREEOPAL
        output_file=new WriterRootTreeOPAL(ai.inputs[1]);
        ((WriterRootTreeOPAL*)(output_file))->init_branches();
        if (options.find("Run")!=options.end()) ((WriterRootTreeOPAL*)(output_file))->set_run_number(std::atoi(options.at("Run").c_str()));
        break;
#else
        printf("Output format %s  is not supported\n",ai.output_format_arg);
        exit(2);
        break;
#endif
    case hpezeus:
#ifdef HEPMCCONVERT_EXTENSION_HEPEVTZEUS
        output_file=new WriterHEPEVTZEUS(ai.inputs[1]);
        break;
#else
        printf("Output format %s  is not supported\n",ai.output_format_arg);
        exit(2);
#endif
    case dot:
#ifdef HEPMCCONVERT_EXTENSION_DOT 
       output_file=new WriterDOT(ai.inputs[1]);
       if (options.find("Style")!=options.end()) ((WriterDOT*)(output_file))->set_style(std::atoi(options.at("Style").c_str()));
       break;
#else
        printf("Output format %s  is not supported\n",ai.output_format_arg);
        exit(2);
        break;
#endif
    case dump:
        output_file=NULL;
        break;
    case none:
        output_file=NULL;
        ignore_writer=true;
        break;
    default:
        printf("Output format %s  is not known\n",ai.output_format_arg);
        exit(2);
        break;
    }
    while( !input_file->failed() )
    {
        GenEvent evt(Units::GEV,Units::MM);
        input_file->read_event(evt);
        if( input_file->failed() )  {
            printf("End of file reached. Exit.\n");
            break;
        }
        if (evt.event_number()<first_event_number) continue;
        if (evt.event_number()>last_event_number) continue;
        evt.set_run_info(input_file->run_info());
        //Note the difference between ROOT and Ascii readers. The former read GenRunInfo before first event and the later at the same time as first event.
        if (!ignore_writer) 
        if (output_file)
        { 
        output_file->write_event(evt); 
        }
        else 
        { 
         Print::content(evt);
        }
        evt.clear();
        ++events_parsed;
        if( events_parsed%print_each_events_parsed == 0 ) printf("Events parsed: %li\n",events_parsed);
        if( events_parsed >= events_limit ) {
            printf("Event limit reached:->events_parsed(%li) >= events_limit(%li)<-. Exit.\n",events_parsed , events_limit);
            break;
        }
    }

    if (input_file)   input_file->close();
    if (output_file)  output_file->close();
    return EXIT_SUCCESS;
}
