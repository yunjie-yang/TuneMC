#include "Pythia8/Pythia.h"
#include "pythia_utils.h"

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

  double eCM = pythia.parm("Beams:eCM");

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

  // Block 2 Hists:
  Hist hChargeMulti_udsc("Charge Multiplicity (udsc)",28,1.0,57.0);
  Hist hChargeMulti_b("Charge Multiplicity (b)",28,1.0,57.0);
  Hist hMomentFrac_udsc("Charged Momentum Fraction (udsc)",40,0.0,8.0);
  Hist hMomentFrac_b("Charged Momentum Fraction (b)",40,0.0,8.0);
  Hist hMomentFrac_Dstar("x(D^{*#pm})",20,0.0,1.0);
  Hist hMomentFrac_Bweak("x_{B}^{weak}",20,0.0,1.0);

  // Block 3: hadron counters: 
  // assignement for each bin listed at the end
  int mesons[10] = {0};
  int baryons[9] = {0};
  int charms[9] = {0};
  int beauties[8] = {0};

  int b_baryons[35] =
      {   5122, 5112, 5212, 5222, 5114, 5214, 5224, 5132, 5232, 5312, 5322, 5314, 5324, 5332, 5334,
          5142, 5242, 5412, 5422, 5414, 5424, 5342, 5432, 5434, 5442, 5444, 5512, 5522, 5514, 5524,
          5532, 5534, 5542, 5544, 5554
      };
  int upsilons[12] = 
      {   553, 30553, 100553, 130553, 200553,
          300553,9000553, 9010553, 20555, 120555,
          557, 100557
      };

  /****************************************************/
  /***********  Declear Observables  ******************/
  /****************************************************/

  Thrust thr(2);
  double Thrusts;

  Sphericity sph(1.,2);

  double C_param;
  double D_param;

  double B_W;
  double B_T;

  int nCh_total = 0;

  /*************    Event Loop    *****************/

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

    /********* Sphericity Analysis *************/

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


    int nCh = 0;

    bool charm_process[2]  = {false};
    bool beauty_process[4] = {false};

    bool gbb = false;
    bool Zbb = false;

    /*********** Particle Loop ***************/

    for (int i = 0 ; i < pythia.event.size() ; ++i)
    {
      int id = pythia.event[i].id();

      if (abs(id) == 5)
      {
        bTagged = true;
      }

      /* Block 1 Analysis */
      if (thrust_analyze_good && pythia.event[i].isFinal() && pythia.event[i].isVisible())
      {
        Vec4 part = pythia.event[i].p();
        denominator += part.pAbs();
        if (dot3(part,thrust_vec)>0) b_plus += cross3(part,thrust_vec).pAbs();
        else b_minus += cross3(part,thrust_vec).pAbs();
      }


      /* Block 2 Analysis */
      if (pythia.event[i].isFinal() && pythia.event[i].isCharged()) 
      {
        nCh++;
        double p = pythia.event[i].pAbs();
        double momentumFrac = abs(log(2*p/eCM));
        if (bTagged==false) hMomentFrac_udsc.fill(momentumFrac); 
        if (bTagged==true)  hMomentFrac_b.fill(momentumFrac); 
      }

      if (abs(id) == 413)
      {
        hMomentFrac_Dstar.fill(2*pythia.event[i].pAbs()/eCM);
      }

      if (!pythia.event[i].isFinal() && pythia.event[i].isHadron() && (pythia.event[i].particleDataEntry().heaviestQuark()==5))
      {
        bool Bstays = 0;
        vector<int> dtrs = pythia.event[i].daughterList();
        for (int iDtr = 0 ; iDtr < (int)dtrs.size() ; iDtr++)
        {
          if (pythia.event[dtrs[iDtr]].particleDataEntry().heaviestQuark()==5)
          {
            Bstays = 1;break;
          }
        }

        if (Bstays == 0)
        {
          hMomentFrac_Bweak.fill(2*pythia.event[i].pAbs()/eCM);
        }
      }

      /* Block 3 Analysis */

      /* light mesons */
      if (abs(id)==211) mesons[0]++;
      if (id==111)      mesons[1]++;
      if (abs(id)==321) mesons[2]++;
      if (id==221)      mesons[3]++;
      if (id==331)      mesons[4]++;
      if (abs(id)==213) mesons[5]++;
      if (id==113)      mesons[6]++;
      if (abs(id)==323) mesons[7]++;
      if (id==223)      mesons[8]++;
      if (id==333)      mesons[9]++;

      /* light baryons */
      if (abs(id)==2212) baryons[0]++;
      if (abs(id)==3122) baryons[1]++;
      if (abs(id)==3112) baryons[2]++;
      if (abs(id)==3222) baryons[2]++;
      if (abs(id)==3212) baryons[3]++;
      if (abs(id)==2224) baryons[4]++;
      if (abs(id)==3214) baryons[5]++;
      if (abs(id)==3224) baryons[5]++;
      if (abs(id)==3312) baryons[6]++;
      if (abs(id)==3324) baryons[7]++;
      if (abs(id)==3334) baryons[8]++;

      /* charm rates */
      if (abs(id)==411)  charms[0]++;
      if (abs(id)==421)  charms[1]++;
      if (abs(id)==413)  charms[2]++;
      if (abs(id)==431)  charms[3]++;
      if (  id==4122  )  charm_process[0]=true;
      if (abs(id)==4)
      {
        int mother1 = pythia.event[i].mother1();
        int mother2 = pythia.event[i].mother2();
	if (mother1>0 && mother2==0 && pythia.event[mother1].isGluon())
          charm_process[1]=true;
      }
      if (id==443)    charms[6]++;
      if (id==20443)  charms[7]++;
      if (id==100443) charms[8]++;

      /* beauty rates */
      if (id==521) beauty_process[0]=true;
      if (abs(id)==521 || abs(id)==511) beauties[1]++;
      if (abs(id)==523 || abs(id)==513 || abs(id)==533 ) beauties[2]++;
      if ( id==531 ) beauty_process[1]=true;
      for (int j = 0 ; j < 35 ; j++)
      {
        if (abs(id)==b_baryons[j]) beauty_process[2]=true;
      }
      if (abs(id)==5)
      {
        int mother1 = pythia.event[i].mother1();
        int mother2 = pythia.event[i].mother2();
        if (mother1>0 && mother2==0 && pythia.event[mother1].isGluon()) 
        {
          beauty_process[3]=true;
	  gbb = true;
        }
        if (mother1>0 && mother2==0 && pythia.event[mother1].id()==23)
          Zbb = true;
      }
      for (int k = 0 ; k < 12 ; k++)
      {
        if (abs(id)==upsilons[k]) beauties[7]++;
      } 


    }//end of particle loop

    if (thrust_analyze_good)
    {
        double B_plus  = b_plus  / (2 * denominator);
        double B_minus = b_minus / (2 * denominator);
        B_W = max(B_plus,B_minus);
        B_T = B_plus + B_minus;
    }

    if (charm_process[0]==true) charms[4]++; 
    if (charm_process[1]==true) charms[5]++;

    if (beauty_process[0]==true) beauties[0]++;
    if (beauty_process[1]==true) beauties[3]++;
    if (beauty_process[2]==true) beauties[4]++;
    if (beauty_process[3]==true) beauties[5]++;
    if (gbb && Zbb)              beauties[6]++;


    /*********** Fill Histograms ***************/

    if (bTagged == false)
    {
      hThrusts_udsc.fill(1-Thrusts);
      hC_param_udsc.fill(C_param);
      hD_param_udsc.fill(D_param);
      hB_W_udsc.fill(B_W);
      hB_T_udsc.fill(B_T);
      hChargeMulti_udsc.fill(nCh);
    }

    if (bTagged == true)
    {
      hThrusts_b.fill(1-Thrusts);
      hC_param_b.fill(C_param);
      hD_param_b.fill(D_param);
      hB_W_b.fill(B_W);
      hB_T_b.fill(B_T);
      hChargeMulti_b.fill(nCh);
    }

    nCh_total += nCh;

  }//end of event loop

  /****************************************************/
  /******  Output Parameters in Generation  ***********/
  /****************************************************/

  const int Nparms = 21;
  char parmName[Nparms][256] = {
        "Beams:eCM",
        "TimeShower:alphaSvalue",
        "TimeShower:pTmin",
        "TimeShower:pTminChgQ",
        "StringPT:sigma",
        "StringZ:bLund",
        "StringZ:aExtraSQuark",
        "StringZ:aExtraDiquark",
        "StringZ:rFactC",
        "StringZ:rFactB",
        "StringFlav:probStoUD",
        "StringFlav:probQQtoQ",
        "StringFlav:probSQtoQQ",
        "StringFlav:probQQ1toQQ0",
        "StringFlav:mesonUDvector",
        "StringFlav:mesonSvector",
        "StringFlav:mesonCvector",
        "StringFlav:mesonBvector",
        "StringFlav:etaSup",
        "StringFlav:etaPrimeSup",
        "StringFlav:decupletSup"
  };
  double parmValues[Nparms] = {0};

  for (int i = 0 ; i < Nparms ; i++ )
        {
          parmValues[i] = pythia.parm(parmName[i]);
        }

  cout<<endl;
  for (int i = 0 ; i < Nparms ; i++)
      cout<<parmName[i]<<" = "<<parmValues[i]<<endl;
  cout<<"seed    = "<<seedNumber<<endl;

  /****************************************************/
  /********   Collect Filled Histograms   *************/
  /****************************************************/

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

  Hists.push_back(hChargeMulti_udsc);Nbins.push_back(28);
  Hists.push_back(hChargeMulti_b);Nbins.push_back(28);
  Hists.push_back(hMomentFrac_udsc);Nbins.push_back(40);
  Hists.push_back(hMomentFrac_b);Nbins.push_back(40);
  Hists.push_back(hMomentFrac_Dstar);Nbins.push_back(20);
  Hists.push_back(hMomentFrac_Bweak);Nbins.push_back(20);

  /****************************************************/
  /***********   Output Histograms   ******************/
  /****************************************************/

  ofstream ofstream_bin_content;
  ofstream_bin_content.open(out_bin_content.c_str());

  for (int iHist = 0 ; iHist < Hists.size() ; ++iHist)
  {
    for (int iBin = 0 ; iBin < Nbins[iHist]+2 ; ++iBin)
    {
      ofstream_bin_content<<Hists[iHist].getBinContent(iBin);
      if (iBin != (Nbins[iHist]+1)) ofstream_bin_content<<",";

    }
    ofstream_bin_content<<std::endl;

  } 

  /****************************************************/
  /***********   Output Hadron Rates  *****************/
  /****************************************************/
  Output_Hadron_Rates(mesons,10,ofstream_bin_content);
  Output_Hadron_Rates(baryons,9,ofstream_bin_content);
  Output_Hadron_Rates(charms,9,ofstream_bin_content);
  Output_Hadron_Rates(beauties,8,ofstream_bin_content);

  ofstream_bin_content<<nCh_total<<std::endl;


}
  /*
  Mesons:
  0 pi+/-
  1 pi0
  2 K+/-
  3 eta
  4 eta'
  5 rho+/-
  6 rho0
  7 K* +/-
  8 omega
  9 phi

  Baryons:
  0 p +/-
  1 Lambda
  2 Sigma +/-
  3 Sigma0
  4 Delta++
  5 Sigma*
  6 Xi +/-
  7 Xi*0
  8 Omega

  Charm hadrons:
  0 D+/-
  1 D0
  2 D* +/-
  3 D_s +/-
  4 Lamnda_c+ X
  5 g -> c cbar
  6 J/psi
  7 chi_c1
  8 psi_3685

  Beauty hadrons:
  0 B+ X
  1 B+/-0
  2 B_uds^*
  3 B_s^0 X
  4 B_baryon + X
  5 g -> b bbar
  6 4b
  7 Upsilon 

  */








