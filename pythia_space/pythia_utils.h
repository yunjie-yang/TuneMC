#include <fstream>

  void Output_Hadron_Rates(int *rates, int Nbins, std::ofstream& output)
  {
    for (int iBin = 0 ; iBin < Nbins-1 ; iBin++)
    {
      output<<rates[iBin]<<",";
    }
    output<<rates[Nbins-1]<<std::endl;
  }

