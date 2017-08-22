//
//  ViewController.swift
//  WhatsGood
//
//  Created by Rohit Bandaru on 7/27/17.
//  Copyright © 2017 Rohit Bandaru. All rights reserved.
//

import UIKit
import CoreLocation
import Alamofire
import SwiftyJSON
import Charts

class ViewController: UIViewController, CLLocationManagerDelegate {

    var locationManager: CLLocationManager = CLLocationManager()
    var currentLocation: CLLocation!
    
    var pieChartView: PieChartView!

    var categories = [String]()
    var quantities = [Double]()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        
        let label = UILabel(frame: CGRect(x: 0, y: 50, width: 200, height: 30))
        label.center.x = view.center.x
        label.textColor = .black
        label.font = UIFont (name: "Avenir", size: 30)
        label.textAlignment = .center
        label.text = "Whats Good?"
        
        view.addSubview(label)
        
        locationManager.desiredAccuracy = kCLLocationAccuracyBest
        locationManager.delegate = self
        locationManager.requestWhenInUseAuthorization()
        // gets location only one time
        locationManager.startUpdatingLocation()
        currentLocation = nil
        
        
        
        
    }
    
    func setChart(dataPoints: [String], values: [Double]) {
        print(dataPoints)
        print(values)
        var dataEntries: [ChartDataEntry] = []
        
        for i in 0..<dataPoints.count {
            let dataEntry1 = PieChartDataEntry(value: values[i], label: dataPoints[i])
            dataEntries.append(dataEntry1)
        }
        
        let pieChartDataSet = PieChartDataSet(values: dataEntries, label: "Number of restaurants")
        let pieChartData = PieChartData(dataSet: pieChartDataSet)
        print(pieChartData)
        
        if pieChartView != nil {
            pieChartView.data = pieChartData
        } else {
            print("Doesn’t contain a value.")
        }
        
        //generates random colors
        var colors: [UIColor] = []
        
        for _ in 0..<dataPoints.count {
            let red = Double(arc4random_uniform(256))
            let green = Double(arc4random_uniform(256))
            let blue = Double(arc4random_uniform(256))
            
            let color = UIColor(red: CGFloat(red/255), green: CGFloat(green/255), blue: CGFloat(blue/255), alpha: 1)
            colors.append(color)
        }
        
        pieChartDataSet.colors = colors
    }
    
    

    func locationManager(_ manager: CLLocationManager,
                         didUpdateLocations locations: [CLLocation])
    {
        currentLocation = locations[locations.count - 1]
        print(currentLocation.description)
        locationManager.stopUpdatingLocation()
        
        let latitude:String = "\(currentLocation.coordinate.latitude)"
        let longitude:String = "\(currentLocation.coordinate.longitude)"
        let urlString = "http://127.0.0.1:5000/data/20/"+latitude+"/"+longitude
   
        print(urlString)
        Alamofire.request(urlString).responseJSON { (responseData) -> Void in
            if((responseData.result.value) != nil) {
                let swiftyJsonVar = JSON(responseData.result.value!)
                for (key, subJson) in swiftyJsonVar {
                    self.categories.append(key)
                    if let quantity = subJson.double{
                        self.quantities.append(quantity)
                    }
                }
                
                self.pieChartView = PieChartView(frame: self.view.bounds)
                self.setChart(dataPoints: self.categories, values: self.quantities)
                self.view.addSubview(self.pieChartView!)
            }
        }
        
    
    }

    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

