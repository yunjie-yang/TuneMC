#include "Pythia8/Pythia.h"

using namespace Pythia8;

int main(int argc, char* argv[]) 
{

  /****************************************************/
  /**************   Read Inputs        ****************/
  /****************************************************/

  int seedNumber = std::stoi(argv[1]);
  int Nevents    = std::stoi(argv[2]);

  string parsFile        = argv[3];
  string out_bin_content = argv[4];

  /****************************************************/
  /************** Initializing Pythia  ****************/
  /****************************************************/

  Pythia pythia;
  pythia.readFile(parsFile.c_str());

  pythia.readString("Random:setSeed = on");
  seedNumber++;
  char seed[256];
  sprintf(seed,"Random:seed = %d",seedNumber);
  pythia.readString(seed);

  pythia.init();

  /****************************************************/
  /******** Declear Observable Histograms  ************/
  /****************************************************/

  // Block 1 Hists:
  Hist hThrusts_udsc(" 1 - Thrust (udsc) ", 17, 0.0, 0.425);
  Hist hThrusts_b(" 1 - Thrust (b) ", 17, 0.0, 0.425);
  Hist hC_param_udsc("C Parameter (udsc) ",20,0.0,1.0);
  Hist hC_param_b("C Parameter (b) ",20,0.0,1.0);
  Hist hD_param_udsc("D Parameter (udsc) ",25,0.0,0.8);
  Hist hD_param_b("D Parameter (b) ",25,0.0,0.8);
  Hist hB_W_udsc("Wide Jet Broadening (udsc) ",19,0.,0.285);
  Hist hB_W_b("Wide Jet Broadening (b) ",19,0.015,0.3);
  Hist hB_T_udsc("Total Jet Broadening (udsc) ",19,0.,0.38);
  Hist hB_T_b("Total Jet Broadening (b) ",19,0.02,0.4);


  /****************************************************/
  /***********  Declear Observables  ******************/
  /****************************************************/

  Thrust thr(2);
  double Thrusts;

  Sphericity sph(1.,2);

  for (int iEvent = 0 ; iEvent < Nevents ; ++iEvent)
  {
    if (!pythia.next()) continue;

    bool bTagged = false;

    /*********** Thrust Analysis ***************/

    Vec4 thrust_vec;
    bool thrust_analyze_good = false;

    if (thr.analyze ( pythia.event ))
    {
      thrust_analyze_good = true;
      Thrusts = thr.thrust();
      thrust_vec = thr.eventAxis(1);

    }

    double C_param;
    double D_param;

    if (sph.analyze( pythia.event )) 
    {
      double e1 = sph.eigenValue(1);
      double e2 = sph.eigenValue(2);
      double e3 = sph.eigenValue(3);

      C_param = 3.*( e1*e2 + e2*e3 + e3*e1 );
      D_param = 27. * e1 * e2 * e3;

     }

    double b_plus      = 0.;
    double b_minus     = 0.;
    double denominator = 0.;


    /*********** Particle Loop ***************/

    for (int i = 0 ; i < pythia.event.size() ; ++i)
    {
      int id = pythia.event[i].id();

      if (id == 5 || id == -5)
      {
        bTagged = true;
      }

      if (thrust_analyze_good && pythia.event[i].isFinal() && pythia.event[i].isVisible())
      {
        Vec4 part = pythia.event[i].p();
        denominator += part.pAbs();
        if (dot3(part,thrust_vec)>0) b_plus += cross3(part,thrust_vec).pAbs();
        else b_minus += cross3(part,thrust_vec).pAbs();
      }

    }//end of particle loop


    /*********** Fill Histograms ***************/

    if (bTagged == false)
    {
      hThrusts_udsc.fill(1-Thrusts);
    }

    if (bTagged == true)
    {
      hThrusts_b.fill(1-Thrusts);
    }

  }//end of event loop

  std::vector<Hist> Hists;
  std::vector<int> Nbins;

  Hists.push_back(hThrusts_udsc);Nbins.push_back(17);
  Hists.push_back(hThrusts_b);Nbins.push_back(17);
  Hists.push_back(hC_param_udsc);Nbins.push_back(20);
  Hists.push_back(hC_param_b);Nbins.push_back(20);
  Hists.push_back(hD_param_udsc);Nbins.push_back(25);
  Hists.push_back(hD_param_b);Nbins.push_back(25);
  Hists.push_back(hB_W_udsc);Nbins.push_back(19);
  Hists.push_back(hB_W_b);Nbins.push_back(19);
  Hists.push_back(hB_T_udsc);Nbins.push_back(19);
  Hists.push_back(hB_T_b);Nbins.push_back(19);

  /****************************************************/
  /***********   Output Histograms   ******************/
  /****************************************************/

  std::cout<< Hists[0];
  std::cout<< Hists[1];

  ofstream ofstream_bin_content;
  ofstream_bin_content.open(out_bin_content.c_str(),std::ios::app);

  for (int iHist = 0 ; iHist < Hists.size() ; ++iHist)
  {
    for (int iBin = 0 ; iBin < Nbins[iHist]+2 ; ++iBin)
    {
      ofstream_bin_content<<Hists[iHist].getBinContent(iBin);
      if (iBin != (Nbins[iHist]+1)) ofstream_bin_content<<",";

    }
    ofstream_bin_content<<std::endl;

  } 


}


