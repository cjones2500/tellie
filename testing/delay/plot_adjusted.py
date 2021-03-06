import utils
import os
import ROOT

if __name__=="__main__":
    can_box = []
    p_box = []
    gr = []
    legend = []
    for b in range(12):
        p_box.append(0)
        can_box.append(ROOT.TCanvas("can_box_%02d"%(b+1)))
        legend.append(ROOT.TLegend(0.1,0.6,0.4,0.9))
        legend[b].SetFillColor(0)
    can_all = ROOT.TCanvas("can_all")

    colors = [ROOT.kBlack,ROOT.kMagenta,ROOT.kRed+1,ROOT.kOrange,
              ROOT.kYellow+1,ROOT.kGreen+1,ROOT.kCyan+1,ROOT.kBlue+1]
    
    delay_values = {}
    for line in file("delays.txt",'r').readlines():
        chan = int(line.split()[0])
        delay_values[chan] = float(line.split()[1])

    ctr = 0
    for f in os.listdir("results_with_offsets"):
        bits = f.split("_")
        if len(bits)!=3:
            continue
        box = int(bits[1][-2:])
        chan = int(bits[2].split('.')[0][-2:])
        logical_channel = (box-1)*8 + chan

        results = utils.PickleFile("results_with_offsets/%s"%f.split(".")[0],2)
        results.load()
        
        signal_t = results.get_meta_data("timeform_2")
        signal_v = results.get_data(1)[0]
        
        gr.append(ROOT.TGraph())
        gr[ctr].SetName("Box %02d Channel %02d"%(box,chan))
        gr[ctr].SetLineColor(colors[chan-1])
        
        for i in range(len(signal_t)):
            adjusted_t = signal_t[i] - (delay_values[logical_channel]*1e-9/2.)
#            gr[ctr].SetPoint(i,signal_t[i],signal_v[i])
            gr[ctr].SetPoint(i,adjusted_t,signal_v[i])
        
        can_box[box-1].cd()
        if p_box[box-1]==0:            
            gr[ctr].Draw("al")
            p_box[box-1]=1
            gr[ctr].GetXaxis().SetRangeUser(0.44e-6,0.48e-6)
        else:
            gr[ctr].Draw("l")
        can_box[box-1].Update()
        
        can_all.cd()
        if ctr==0:
            gr[ctr].Draw("al")
        else:
            gr[ctr].Draw("l")
        can_all.Update()                      

        legend[box-1].AddEntry(gr[ctr],gr[ctr].GetName(),"l")

        ctr+=1

    for b in range(12):
        can_box[box-1].cd()
        legend[box-1].Draw()
        can_box[box-1].Update()

    raw_input("wait")
